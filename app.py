import streamlit as st
import time
import os
import re
import requests
from google import genai
from streamlit_lottie import st_lottie
from streamlit_extras.metric_cards import style_metric_cards

# --- 1. CONFIGURATION & ROBUST ANIMATION LOADER ---
st.set_page_config(
    page_title="Forensic Analyst Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Stable Lottie URLs
LOTTIE_SCANNING = "https://assets10.lottiefiles.com/packages/lf20_st79sc61.json"
LOTTIE_WAITING = "https://assets5.lottiefiles.com/packages/lf20_6p8ovm.json"

# Custom CSS for Apple Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #f5f5f7; }
    @keyframes glow {
        0% { box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8); }
        50% { box-shadow: 0 8px 32px 0 rgba(0, 113, 227, 0.15); }
        100% { box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8); }
    }
    .report-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        margin-top: 20px;
        animation: glow 4s infinite alternate;
    }
    h1 {
        background: linear-gradient(180deg, #FFFFFF 0%, #A1A1A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
    }
    div.stButton > button:first-child {
        background-color: #0071e3;
        color: white;
        border-radius: 980px;
        padding: 14px 40px;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    .meter-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 6px;
        width: 100%;
        margin-top: 12px;
        overflow: hidden;
    }
    .meter-fill { height: 100%; border-radius: 10px; transition: width 2s ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FRONT END LAYOUT ---
left_spacer, col1, col2, right_spacer = st.columns([0.1, 1, 1, 0.1])

with col1:
    st.title("Forensic Analysis.")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem;'>Advanced Deepfake & Redistribution Engine</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=["mp4", "mov"])
    
    if uploaded_file:
        st.video(uploaded_file)
        with st.expander("🔬 Detection Methodology"):
            st.write("Analyzing biological motion and temporal consistency for official sports media integrity.")

with col2:
    st.write("## \n## ") 
    
    if uploaded_file:
        if st.button("Initialize Deep Scan"):
            temp_path = "temp_video.mp4"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.status("Performing Multi-Layer Audit...", expanded=True) as status:
                try:
                    # SECURE KEY RETRIEVAL
                    # Locally: Use st.secrets or replace with your new key string temporarily
                    api_key = st.secrets.get("GEMINI_API_KEY", "PASTE_NEW_KEY_HERE_IF_LOCAL")
                    client = genai.Client(api_key=api_key)
                    
                    scan_anim = load_lottieurl(LOTTIE_SCANNING)
                    if scan_anim: st_lottie(scan_anim, height=150, key="scanning")
                    
                    instruction = """
                    You are a Sports Media Integrity Expert.
                    Analyze for deepfakes AND unauthorized redistribution signatures (watermarks, restreaming UI).
                    You MUST end with:
                    FINAL_VERDICT: [AUTHENTIC, MANIPULATED, or UNAUTHORIZED REDISTRIBUTION]
                    CONFIDENCE_SCORE: [Number]%
                    """
                    
                    st.write("📤 Uploading...")
                    gemini_file = client.files.upload(file=temp_path)
                    
                    while gemini_file.state.name == "PROCESSING":
                        time.sleep(2)
                        gemini_file = client.files.get(name=gemini_file.name)
                    
                    st.write("🧠 Executing Forensic Logic...")
                    response = client.models.generate_content(
                        model="gemini-3.1-pro-preview",
                        config={'system_instruction': instruction},
                        contents=[gemini_file, "Audit this sports clip for content integrity and distribution rights."]
                    )
                    
                    status.update(label="Analysis Complete", state="complete", expanded=False)
                    
                    # Parsing
                    res_upper = response.text.upper()
                    if "FINAL_VERDICT: AUTHENTIC" in res_upper:
                        v_color, v_label = "#34c759", "Authentic"
                    elif "FINAL_VERDICT: MANIPULATED" in res_upper:
                        v_color, v_label = "#ff3b30", "Manipulated"
                    elif "FINAL_VERDICT: UNAUTHORIZED" in res_upper:
                        v_color, v_label = "#ff9500", "Unauthorized"
                    else:
                        v_color, v_label = "#86868b", "Inconclusive"
                    
                    conf = int(re.search(r'CONFIDENCE_SCORE:\s*(\d+)', res_upper).group(1)) if re.search(r'CONFIDENCE_SCORE:\s*(\d+)', res_upper) else 100

                    # Metrics
                    m1, m2 = st.columns(2)
                    m1.metric("System Verdict", v_label)
                    m2.metric("Confidence Level", f"{conf}%")
                    style_metric_cards(background_color="rgba(255,255,255,0.05)", border_left_color=v_color)

                    st.markdown(f"""<div class="report-card">
                        <p style='color: #86868b; font-size: 0.8rem;'>Neural Confidence Scan</p>
                        <div class="meter-container"><div class="meter-fill" style="width: {conf}%; background-color: {v_color};"></div></div>
                    </div>""", unsafe_allow_html=True)

                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Engine Failure: {e}")
                finally:
                    if os.path.exists(temp_path): os.remove(temp_path)
    else:
        wait_anim = load_lottieurl(LOTTIE_WAITING)
        if wait_anim: st_lottie(wait_anim, height=250, key="waiting")
        st.info("Awaiting media input for digital integrity audit.")

st.markdown("<br><br><p style='text-align: center; color: #424245; font-size: 0.8rem;'>Digital Sports Integrity Framework • IIT Bhilai • Built with Gemini 3.1 Pro</p>", unsafe_allow_html=True)
