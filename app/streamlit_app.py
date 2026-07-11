import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Support Ticket Triage", page_icon="🎫", layout="wide")

st.markdown("""
<style>
.stApp {
    background: #FFFFFF !important;
}
h1, h1 * {
    color: #13233F !important;
}
p, .stCaption, [data-testid="stCaptionContainer"] {
    color: #5B6B82 !important;
}
.main .block-container {
    padding-top: 2rem; 
    max-width: 900px;
}
label, .stSelectbox label, .stTextInput label, .stCheckbox label {
    color: #1F2937 !important;
    font-weight: 600 !important;
}
div[data-baseweb="select"] > div, .stTextInput input {
    background-color: #F5F7FA !important;
    color: #1F2937 !important;
    border: 1px solid #D9DEE6 !important;
}
.risk-card {
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-top: 1rem;
    font-size: 1.1rem;
    font-weight: 600;
}
.risk-high {background-color: #FDECEC; border-left: 6px solid #D64550; color: #9B2C2C;}
.risk-medium {background-color: #FEF3E2; border-left: 6px solid #E8A33D; color: #92400E;}
.risk-low {background-color: #E9F7EE; border-left: 6px solid #2FA84F; color: #1E6B36;}
</style>
""", unsafe_allow_html=True)

st.title("🎫 Support Ticket Triage")
st.caption("Predicts SLA-breach risk for incoming consumer complaints using a LightGBM model trained on CFPB complaint data.")

API_URL = "https://support-ticket-triage.onrender.com/predict"

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
        response = requests.post(API_URL, json=payload, timeout=30)
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
        st.error("⚠️ Could not connect to the API. The backend service may be starting up — please try again in 30-60 seconds.")
    except Exception as e:
        st.error(f"Error: {e}")