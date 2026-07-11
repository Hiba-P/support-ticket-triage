import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Support Ticket Triage", page_icon="🎫", layout="wide")

st.markdown("""
<style>
.stApp {
    background: 
        radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 80% 80%, rgba(34, 197, 94, 0.1) 0%, transparent 40%),
        linear-gradient(135deg, #0a0f1e 0%, #131b2e 50%, #0a0f1e 100%);
    background-attachment: fixed;
}
.main .block-container {
    padding-top: 2rem; 
    max-width: 900px;
    background: rgba(20, 27, 45, 0.6);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.05);
}
.risk-card {
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-top: 1rem;
    font-size: 1.1rem;
    font-weight: 600;
}
.risk-high {background-color: #3d1a1a; border-left: 6px solid #ff4b4b; color: #ffb3b3;}
.risk-medium {background-color: #3d2f0f; border-left: 6px solid #ffa500; color: #ffd580;}
.risk-low {background-color: #10331a; border-left: 6px solid #21c354; color: #8ce8a8;}
h1 {font-size: 2.2rem !important;}
</style>
""", unsafe_allow_html=True)

st.title("🎫 Support Ticket Triage")
st.caption("Predicts SLA-breach risk for incoming consumer complaints using a LightGBM model trained on CFPB complaint data.")

API_URL = "http://127.0.0.1:8000/predict"

col1, col2 = st.columns(2)

with col1:
    product = st.selectbox("📦 Product", ["Debt collection", "Credit card"])
    issue = st.selectbox("⚠️ Issue", [
        "Attempts to collect debt not owed",
        "Written notification about debt",
        "Took or threatened to take negative or legal action",
        "Communication tactics",
        "Fees or interest",
        "Problem with a purchase shown on your statement",
        "Other"
    ])
    state = st.text_input("📍 State (2-letter code)", "PA", max_chars=2)

with col2:
    sub_product = st.text_input("🏷️ Sub-product", "Medical debt")
    has_narrative = st.checkbox("📝 Complaint includes narrative", value=True)

st.write("")
submitted = st.button("🔍 Predict Risk", use_container_width=True, type="primary")

if submitted:
    now = datetime.now().isoformat()
    payload = {
        "product": product,
        "sub_product": sub_product,
        "issue": issue,
        "state": state,
        "date_received": now,
        "date_sent_to_company": now,
        "has_narrative": has_narrative
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()

        proba = result["late_probability"]
        risk = result["risk_level"]

        st.write("")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Late Probability", f"{proba*100:.1f}%")
        with m2:
            st.progress(min(proba, 1.0))

        risk_labels = {
            "high": ("🔴 HIGH RISK", "recommend immediate escalation", "risk-high"),
            "medium": ("🟠 MEDIUM RISK", "recommend monitoring", "risk-medium"),
            "low": ("🟢 LOW RISK", "standard processing queue", "risk-low"),
        }
        label, action, css_class = risk_labels[risk]

        st.markdown(f"""
        <div class="risk-card {css_class}">
            {label} — {action}
        </div>
        """, unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Could not connect to the API. Make sure the FastAPI server is running on port 8000.")
    except Exception as e:
        st.error(f"Error: {e}")
        