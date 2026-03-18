import streamlit as st
import time
import os
import re
import requests
from google import genai
from streamlit_lottie import st_lottie

# --- 1. GLOBAL PAGE SETUP ---
st.set_page_config(page_title="Forensic Analyst Ultra", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE ULTIMATE CSS (No more ghost bars) ---
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

    /* Target the specific container where content lives */
    [data-testid="stVerticalBlock"] > div:has(div.glass-card) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(40px) saturate(150%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
    }

    [data-testid="stHeader"] { display: none !important; }
    
    .ultra-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 4.5rem !important;
        letter-spacing: -3px;
        background: linear-gradient(to bottom, #fff 50%, rgba(255,255,255,0.2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        line-height: 1;
    }

    .subtitle {
        color: #86868b; 
        font-size: 1.2rem; 
        margin-top: 5px; 
        margin-bottom: 40px;
    }
    
    /* This invisible marker helps us target the container with CSS */
    .glass-card { display: none; }

    div[role="radiogroup"] {
        background: rgba(255,255,255,0.05);
        padding: 8px;
        border-radius: 12px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #0071e3, #00c6ff) !important;
        border: none !important;
        color: white !important;
        border-radius: 100px !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

def load_lottie(url):
    try: 
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- 3. FRONT END ---
st.markdown("<h1 class='ultra-title'>Forensic.</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Digital Sports Integrity Framework</p>", unsafe_allow_html=True)

# THE FIX: Wrap everything in one container with an invisible marker
with st.container():
    st.markdown('<div class="glass-card"></div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.write("### Data Input")
        input_type = st.radio("Media Source", ["📁 Upload File", "🔗 Video URL"], horizontal=True, label_visibility="collapsed")
        
        file = None
        media_ready = False

        if input_type == "📁 Upload File":
            file = st.file_uploader("", type=["mp4", "mov"], label_visibility="collapsed")
            if file:
                st.video(file)
                media_ready = True
        else:
            video_url = st.text_input("Paste video link...", placeholder="YouTube, Twitter, public MP4")
            if video_url:
                try:
                    st.video(video_url)
                    media_ready = True
                except:
                    st.error("Invalid video link.")

        if not media_ready:
            anim_waiting = load_lottie("https://assets5.lottiefiles.com/packages/lf20_6p8ovm.json")
            if anim_waiting: st_lottie(anim_waiting, height=200)
            else: st.info("Waiting for media uplink...")

    with col_right:
        if media_ready:
            st.write("### Analysis Engine")
            if st.button("EXECUTE QUANTUM AUDIT"):
                st.status("🔮 Analyzing...")
        else:
            st.write("### System Status")
            st.markdown("🟢 **Neural Engine:** Active")
            st.markdown("🔵 **Uplink:** Waiting for input...")
            
            anim_status = load_lottie("https://assets10.lottiefiles.com/packages/lf20_st79sc61.json")
            if anim_status: st_lottie(anim_status, height=200)

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.1); font-size: 0.8rem; margin-top: 50px;'>IIT BHILAI • GDG SOLUTION CHALLENGE 2026</p>", unsafe_allow_html=True)
