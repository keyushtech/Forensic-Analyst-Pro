import streamlit as st
import time
import os
import re
from google import genai

# --- 1. APPLE AESTHETIC CONFIGURATION ---
st.set_page_config(
    page_title="Forensic Analyst Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the Apple "Midnight" look + Animations
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background-color: #000000;
        color: #f5f5f7;
    }

    /* Modern Glassmorphism Card with subtle pulse */
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

    /* Apple San Francisco Typography */
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    h1 {
        background: linear-gradient(180deg, #FFFFFF 0%, #A1A1A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Custom Blue Action Button */
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
        box-shadow: 0 4px 20px rgba(0, 113, 227, 0.4);
    }

    /* Confidence Meter Visuals */
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
        transition: width 1.5s ease-in-out;
    }

    /* File Uploader Customization */
    .stFileUploader {
        border: 1px dashed rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FRONT END LAYOUT ---
# Using columns to create a balanced, wide look
left_spacer, col1, col2, right_spacer = st.columns([0.1, 1, 1, 0.1])

with col1:
    st.title("Forensic Analysis.")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem;'>Advanced Deepfake Detection Engine</p>", unsafe_allow_html=True)
    
    # Drag and Drop
    uploaded_file = st.file_uploader("", type=["mp4", "mov"])
    
    if uploaded_file:
        st.video(uploaded_file)
        
        # Adding a professional methodology dropdown 
        with st.expander("🔬 Detection Methodology"):
            st.write("This engine utilizes a **Null Hypothesis Framework**. It actively attempts to attribute visual anomalies to standard h.264 compression, motion blur, and broadcast CGI before declaring a spatial or temporal physics violation.")

with col2:
    st.write("## ") # Push content down to align with header
    st.write("## ") 
    
    if uploaded_file:
        if st.button("Initialize Deep Scan"):
            
            temp_path = "temp_video.mp4"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.status("Analyzing Media Integrity...", expanded=True) as status:
                try:
                    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
                    st.write("🛰️ Connecting to Neural Engine...")
                    instruction = """
                    You are a highly conservative Digital Video Analyst. 
                    1. THE NULL HYPOTHESIS: Your default assumption is that the video is REAL.
                    2. IGNORE BROADCAST GRAPHICS: Ignore scorecards, lower-thirds, and CGI logos. 
                    3. FOCUS ON SUBJECTS: Look for AI signatures ONLY in human features.
                    4. COMPRESSION VS. AI: Do not mistake motion blur or macroblocking for AI.
                    """
                    
                    st.write("📤 Uploading frames for pixel-level inspection...")
                    gemini_file = client.files.upload(file=temp_path)
                    
                    while gemini_file.state.name == "PROCESSING":
                        time.sleep(2)
                        gemini_file = client.files.get(name=gemini_file.name)
                    
                    st.write("🧠 Running Forensic Logic...")
                    user_prompt = """
                    Analyze this video by strictly following these steps:
                    Step 1: Describe the scene objectively.
                    Step 2: Note any visual anomalies.
                    Step 3: Explain how standard compression or motion blur could cause the anomalies.
                    Step 4: Provide your final verdict (REAL or AI-GENERATED) and a Confidence Score.
                    """
                    
                    response = client.models.generate_content(
                        model="gemini-3.1-pro-preview",
                        config={'system_instruction': instruction},
                        contents=[gemini_file, user_prompt]
                    )
                    
                    status.update(label="Analysis Complete", state="complete", expanded=False)
                    
                    # --- THE VERDICT DISPLAY ---
                    is_real = "VERDICT: REAL" in response.text.upper()
                    verdict_color = "#34c759" if is_real else "#ff3b30" # Apple Green vs Apple Red
                    verdict_text = "Authentic (Original)" if is_real else "Suspicious (Manipulated)"
                    
                    # Regex to hunt down the confidence score number the AI outputs
                    match = re.search(r'Confidence Score:\s*(\d+)', response.text, re.IGNORECASE)
                    confidence = int(match.group(1)) if match else 100

                    # The new styled report card with the dynamic progress bar
                    st.markdown(f"""
                        <div class="report-card">
                            <h3 style='color: {verdict_color}; margin-top: 0; margin-bottom: 5px;'>{verdict_text}</h3>
                            <p style='color: #86868b; font-size: 0.9rem; margin-bottom: 5px; font-weight: 600;'>Confidence Level: {confidence}%</p>
                            <div class="meter-container">
                                <div class="meter-fill" style="width: {confidence}%; background-color: {verdict_color};"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # Streamlit's native markdown renderer handles the bolding beautifully
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Engine Failure: {e}")
                
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
    else:
        st.info("Please upload a video file to begin forensic processing.")

# --- 3. THE FOOTER ---
st.markdown("<br><br><p style='text-align: center; color: #424245; font-size: 0.8rem;'>Hardware Accelerated Forensic Analysis • Built with Gemini 3.1 Pro</p>", unsafe_allow_html=True)
