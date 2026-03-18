import streamlit as st
import time
import os
import requests
from google import genai
from streamlit_lottie import st_lottie

# --- 1. GLOBAL PAGE SETUP ---
st.set_page_config(page_title="Forensic Analyst Ultra", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE FINAL CSS (Bar-Free Edition) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, rgba(60, 10, 80, 0.7) 0px, transparent 50%),
            radial-gradient(at 80% 10%, rgba(120, 10, 50, 0.6) 0px, transparent 50%),
            radial-gradient(at 20% 90%, rgba(10, 90, 60, 0.5) 0px, transparent 50%),
            radial-gradient(at 90% 90%, rgba(0, 50, 120, 0.6) 0px, transparent 50%);
        background-attachment: fixed;
    }

    /* 1. HIDE DEFAULT STREAMLIT TOP BARS */
    [data-testid="stHeader"], [data-testid="stDecoration"] { display: none !important; }
    .block-container { padding-top: 3rem !important; }

    /* 2. KILL THE SHADOW BAR: Force all vertical blocks to be transparent */
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    
    /* 3. THE GLASS CARD: Target the inner container specifically */
    .main-glass-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(40px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(150%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 28px !important;
        padding: 40px !important;
        margin-top: 20px !important;
    }

    .ultra-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 5rem !important;
        letter-spacing: -3px;
        color: white;
        margin-bottom: 0px;
        line-height: 1;
    }

    .subtitle {
        color: #86868b; 
        font-size: 1.1rem; 
        margin-top: 10px;
    }

    /* Styling the Radio Buttons to look like Apple toggles */
    div[role="radiogroup"] {
        background: rgba(255,255,255,0.05) !important;
        padding: 5px !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

def load_lottie(url):
    try: return requests.get(url, timeout=5).json()
    except: return None

# --- 3. FRONT END ---
st.markdown("<h1 class='ultra-title'>Forensic.</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Digital Sports Integrity Framework</p>", unsafe_allow_html=True)

# The "Bar Killer" wrapper
with st.container():
    # We apply the custom class here via markdown
    st.markdown('<div class="main-glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.write("### Data Input")
        input_type = st.radio("Media Source", ["📁 Upload File", "🔗 Video URL"], horizontal=True, label_visibility="collapsed")
        
        file = st.file_uploader("", type=["mp4", "mov"], label_visibility="collapsed") if "Upload" in input_type else st.text_input("Paste video link...", placeholder="YouTube, Twitter, public MP4")
        
        if not file:
            st.info("Waiting for media uplink...")

    with col2:
        st.write("### System Status")
        st.markdown("🟢 **Neural Engine:** Active")
        st.markdown("🔵 **Uplink:** Waiting for input...")
        
        # Load a smaller, cleaner status animation
        anim = load_lottie("https://assets10.lottiefiles.com/packages/lf20_st79sc61.json")
        if anim: st_lottie(anim, height=150)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.1); font-size: 0.8rem; margin-top: 60px;'>IIT BHILAI • GDG SOLUTION CHALLENGE 2026</p>", unsafe_allow_html=True)
