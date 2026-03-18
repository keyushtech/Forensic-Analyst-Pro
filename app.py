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

# Stable Lottie URLs (Community Assets)
LOTTIE_SCANNING = "https://assets10.lottiefiles.com/packages/lf20_st79sc61.json"
LOTTIE_WAITING = "https://assets5.lottiefiles.com/packages/lf20_6p8ovm.json"

# Custom CSS for the Apple "Midnight" look
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
        margin-bottom: 20px;
        animation: glow 4s infinite alternate;
    }

    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
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
        font-size: 16px;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #0077ed;
        transform: scale(1.02);
    }

    .meter-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 6px;
        width: 100%;
        margin-top: 12px;
        overflow: hidden;
    }
    .meter-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 2s ease-in-out;
    }
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
            st.write("This engine analyzes biological motion, temporal consistency, and unauthorized watermark overlays to ensure the **Integrity of Digital Sports Media**.")

with col2:
    st.write("## \n## ") 
    
    if uploaded_file:
        if st.button("Initialize Deep Scan"):
            temp_path = "temp_video.mp4"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.status("Performing Multi-Layer Audit...", expanded=True) as status:
                try:
                    client = genai.Client(api_key='AIzaSyDD4L7TnfAoXiB96P3Gdlki-_KPqtFwWVA')
                    
                    # Safe Animation Loading
                    scan_anim = load_lottieurl(LOTTIE_SCANNING)
                    if scan_anim:
                        st_lottie(scan_anim, height=150, key="scanning")
                    
                    instruction = """
                    You are a Sports Media Integrity Expert.
                    1. ANALYSIS: Look for AI artifacts in faces/motion AND unauthorized logos or pirate stream overlays.
                    2. VERDICT RULES: 
                       - If original: FINAL_VERDICT: AUTHENTIC
                       - If deepfake: FINAL_VERDICT: MANIPULATED
                       - If pirated/restreamed: FINAL_VERDICT: UNAUTHORIZED REDISTRIBUTION
                    3. FORMAT: You MUST end with exactly:
                       FINAL_VERDICT: [RESULT]
                       CONFIDENCE_SCORE: [Number]%
                    """
                    
                    st.write("📤 Uploading to Neural Engine...")
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
                    
                    # --- ROBUST PARSING ENGINE ---
                    response_text = response.text.upper()
                    
                    if "FINAL_VERDICT: AUTHENTIC" in response_text:
                        verdict_color = "#34c759"
                        verdict_label = "Authentic"
                    elif "FINAL_VERDICT: MANIPULATED" in response_text:
                        verdict_color = "#ff3b30"
                        verdict_label = "Manipulated (Fake)"
                    elif "FINAL_VERDICT: UNAUTHORIZED" in response_text:
                        verdict_color = "#ff9500"
                        verdict_label = "Unauthorized Redistribution"
                    else:
                        verdict_color = "#86868b"
                        verdict_label = "Inconclusive"
                    
                    match = re.search(r'CONFIDENCE_SCORE:\s*(\d+)', response_text)
                    confidence = int(match.group(1)) if match else 100

                    # METRICS DISPLAY
                    m_col1, m_col2 = st.columns(2)
                    with m_col1:
                        st.metric(label="System Verdict", value=verdict_label)
                    with m_col2:
                        st.metric(label="Confidence Level", value=f"{confidence}%")
                    style_metric_cards(background_color="rgba(255,255,255,0.05)", border_left_color=verdict_color)

                    st.markdown(f"""
                        <div class="report-card">
                            <p style='color: #86868b; font-size: 0.9rem; margin-bottom: 5px; font-weight: 600;'>Neural Confidence Scan</p>
                            <div class="meter-container">
                                <div class="meter-fill" style="width: {confidence}%; background-color: {verdict_color};"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Engine Failure: {e}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
    else:
        wait_anim = load_lottieurl(LOTTIE_WAITING)
        if wait_anim:
            st_lottie(wait_anim, height=250, key="waiting")
        st.info("Awaiting media input for digital integrity audit.")

st.markdown("<br><br><p style='text-align: center; color: #424245; font-size: 0.8rem;'>Digital Sports Integrity Framework • IIT Bhilai • Built with Gemini 3.1 Pro</p>", unsafe_allow_html=True)
