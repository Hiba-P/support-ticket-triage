import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Support Ticket Triage", page_icon="🎫", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #131b2e 50%, #0a0f1e 100%) !important;
}
h1, h1 * {
    color: #FFFFFF !important;
}
p, .stCaption, [data-testid="stCaptionContainer"] {
    color: #CADCFC !important;
}
.main .block-container {
    padding-top: 2rem; 
    max-width: 900px;
    background: rgba(20, 27, 45, 0.85);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    border: 1px solid rgba(255,255,255,0.08);
}
label, .stSelectbox label, .stTextInput label, .stCheckbox label {
    color: #E8EDF5 !important;
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
</style>
""", unsafe_allow_html=True)