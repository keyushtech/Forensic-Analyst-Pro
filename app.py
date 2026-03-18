import streamlit as st
import time
import os
import re
import requests
import pandas as pd
import numpy as np
from google import genai
from streamlit_lottie import st_lottie
from streamlit_extras.metric_cards import style_metric_cards

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Forensic Analyst Pro", page_icon="🔍", layout="wide", initial_sidebar_state="collapsed")

def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

LOTTIE_SCANNING = "https://assets10.lottiefiles.com/packages/lf20_st79sc61.json"
LOTTIE_WAITING = "https://assets5.lottiefiles.com/packages/lf20_6p8ovm.json"

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #f5f5f7; }
    .report-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
    }
    h1 { background: linear-gradient(180deg, #FFFFFF 0%, #A1A1A1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem !important; }
    div.stButton > button:first-child { background-color: #0071e3; color: white; border-radius: 980px; padding: 12px 30px; width: 100%; border: none; }
    .meter-container { background: rgba(255,255,255,0.1); border-radius: 10px; height: 6px; width: 100%; margin-top: 10px; overflow: hidden; }
    .meter-fill { height: 100%; border-radius: 10px; transition: width 2s ease-in-out; }
    </style>
""", unsafe_allow_html=True)

# --- 2. LAYOUT ---
l_sp, col1, col2, r_sp = st.columns([0.1, 1, 1, 0.1])

with col1:
    st.title("Forensic Analysis.")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem;'>Digital Sports Integrity Framework</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["mp4", "mov"])
    if uploaded_file:
        st.video(uploaded_file)
        with st.expander("🔬 Detection Methodology"):
            st.write("Cross-referencing spatial artifacts with temporal redistribution signatures.")

with col2:
    st.write("## \n## ")
    if uploaded_file:
        if st.button("Initialize Deep Scan"):
            temp_path = "temp_video.mp4"
            with open(temp_path, "wb") as f: f.write(uploaded_file.getbuffer())
            
            with st.status("Performing Multi-Layer Audit...", expanded=True) as status:
                try:
                    # SECURE KEY ACCESS
                    api_key = st.secrets.get("GEMINI_API_KEY", "PASTE_NEW_KEY_HERE_FOR_LOCAL_TEST")
                    client = genai.Client(api_key=api_key)
                    
                    anim = load_lottieurl(LOTTIE_SCANNING)
                    if anim: st_lottie(anim, height=120, key="scan")
                    
                    instruction = """
                    You are a Sports Media Expert. Analyze for fakes AND unauthorized restreaming indicators (low bitrate, non-official logos, camera-on-screen).
                    End with: 
                    FINAL_VERDICT: [AUTHENTIC, MANIPULATED, or UNAUTHORIZED REDISTRIBUTION]
                    CONFIDENCE_SCORE: [Number]%
                    """
                    
                    gemini_file = client.files.upload(file=temp_path)
                    while gemini_file.state.name == "PROCESSING":
                        time.sleep(2)
                        gemini_file = client.files.get(name=gemini_file.name)
                    
                    response = client.models.generate_content(
                        model="gemini-3.1-pro-preview",
                        config={'system_instruction': instruction},
                        contents=[gemini_file, "Audit this sports clip for content integrity and distribution rights."]
                    )
                    
                    status.update(label="Audit Complete", state="complete", expanded=False)
                    
                    res_upper = response.text.upper()
                    if "AUTHENTIC" in res_upper: v_color, v_label = "#34c759", "Authentic"
                    elif "MANIPULATED" in res_upper: v_color, v_label = "#ff3b30", "Manipulated"
                    elif "UNAUTHORIZED" in res_upper: v_color, v_label = "#ff9500", "Unauthorized"
                    else: v_color, v_label = "#86868b", "Inconclusive"
                    
                    conf_match = re.search(r'CONFIDENCE_SCORE:\s*(\d+)', res_upper)
                    conf = int(conf_match.group(1)) if conf_match else 100

                    # Metrics & Visuals
                    m1, m2 = st.columns(2)
                    m1.metric("System Verdict", v_label)
                    m2.metric("Confidence", f"{conf}%")
                    style_metric_cards(background_color="rgba(255,255,255,0.05)", border_left_color=v_color)

                    st.markdown(f"""<div class="report-card">
                        <p style='color: #86868b; font-size: 0.8rem;'>Confidence Bar</p>
                        <div class="meter-container"><div class="meter-fill" style="width: {conf}%; background-color: {v_color};"></div></div>
                    </div>""", unsafe_allow_html=True)

                    st.markdown(response.text)

                    # EXTRA TOOL: Leak Map
                    if v_label == "Unauthorized Redistribution":
                        st.write("---")
                        st.write("### 🌍 Distribution Leak Map")
                        map_data = pd.DataFrame(np.random.randn(5, 2) / [50, 50] + [21.1458, 79.0882], columns=['lat', 'lon'])
                        st.map(map_data)

                except Exception as e: st.error(f"Error: {e}")
                finally: 
                    if os.path.exists(temp_path): os.remove(temp_path)
    else:
        anim = load_lottieurl(LOTTIE_WAITING)
        if anim: st_lottie(anim, height=250, key="wait")
        st.info("Awaiting media input for integrity audit.")

st.markdown("<br><p style='text-align: center; color: #424245; font-size: 0.8rem;'>Digital Sports Integrity Framework • IIT Bhilai • Built with Gemini 3.1 Pro</p>", unsafe_allow_html=True)
