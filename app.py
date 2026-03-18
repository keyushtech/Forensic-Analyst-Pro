import streamlit as st
import time
import os
import re
import requests
from google import genai
from streamlit_lottie import st_lottie

# --- 1. GLOBAL PAGE SETUP ---
st.set_page_config(page_title="Forensic Analyst Ultra", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE LIQUID GLASS ENGINE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    /* Animated Liquid Mesh Background */
    .stApp {
        background: radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                    radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                    radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
        background-color: #050505;
        background-attachment: fixed;
        overflow: hidden;
    }

    /* The Liquid Glass Card */
    .liquid-glass {
        background: rgba(255, 255, 255, 0.01);
        backdrop-filter: blur(40px) saturate(200%);
        -webkit-backdrop-filter: blur(40px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 50px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
    }
    .liquid-glass:hover {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform: translateY(-5px);
    }

    /* Shimmering Title */
    .ultra-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 5rem !important;
        letter-spacing: -3px;
        background: linear-gradient(to bottom, #fff 30%, rgba(255,255,255,0.1));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* Liquid Button */
    div.stButton > button {
        background: linear-gradient(90deg, #0071e3, #00c6ff) !important;
        border: none !important;
        color: white !important;
        padding: 20px 40px !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        border-radius: 100px !important;
        box-shadow: 0 10px 30px rgba(0, 113, 227, 0.3) !important;
        transition: all 0.4s !important;
    }
    div.stButton > button:hover {
        transform: scale(1.05) rotate(-1deg);
        box-shadow: 0 15px 40px rgba(0, 113, 227, 0.6) !important;
    }

    /* Custom Scrollbar for the Apple feel */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC HELPER ---
def load_lottie(url):
    try: return requests.get(url).json()
    except: return None

# --- 4. FRONT END ---
st.markdown("<h1 class='ultra-title'>Forensic.</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #86868b; font-size: 1.5rem; margin-top:-20px; font-weight:400;'>Advanced Media Integrity Engine</p>", unsafe_allow_html=True)

# Main Container
st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    file = st.file_uploader("", type=["mp4", "mov"])
    if file:
        st.video(file)
    else:
        # Beautiful "Empty State" Lottie
        lottie_waiting = load_lottie("https://assets5.lottiefiles.com/packages/lf20_6p8ovm.json")
        if lottie_waiting: st_lottie(lottie_waiting, height=400)

with col_right:
    st.write("## ")
    if file:
        if st.button("EXECUTE QUANTUM AUDIT"):
            with st.status("🔮 Analyzing Light Physics...", expanded=True) as s:
                try:
                    # Retrieve the secret key you set up earlier
                    # If local, you can still use the string temporarily
                    api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyDD4L7TnfAoXiB96P3Gdlki-_KPqtFwWVA")
                    client = genai.Client(api_key=api_key)

                    # Save and Upload
                    with open("temp.mp4", "wb") as f: f.write(file.getbuffer())
                    g_file = client.files.upload(file="temp.mp4")
                    
                    while g_file.state.name == "PROCESSING":
                        time.sleep(2)
                        g_file = client.files.get(name=g_file.name)
                    
                    response = client.models.generate_content(
                        model="gemini-3.1-pro-preview",
                        contents=[g_file, "Is this video real or a deepfake? Be highly technical."]
                    )
                    
                    s.update(label="Audit Complete", state="complete")
                    
                    # Result UI
                    st.markdown("### 🧬 Analysis Report")
                    st.write(response.text)
                    
                except Exception as e: st.error(f"Engine Failure: {e}")
    else:
        st.info("System Ready. Waiting for encrypted media uplink...")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.2); font-size: 0.8rem; margin-top: 50px;'>HARWARE ACCELERATED • GEMINI 3.1 PRO • IIT BHILAI</p>", unsafe_allow_html=True)
