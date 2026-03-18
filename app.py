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

    .stApp {
        background: radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                    radial-gradient(at 100% 0%, hsla(225,39%,20%,1) 0, transparent 50%);
        background-color: #050505;
        background-attachment: fixed;
    }

    .block-container { padding-top: 2rem !important; }
    .stMarkdown div { background: none !important; }

    .ultra-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 4.5rem !important;
        letter-spacing: -3px;
        background: linear-gradient(to bottom, #fff 50%, rgba(255,255,255,0.2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    .liquid-glass {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(40px) saturate(150%);
        -webkit-backdrop-filter: blur(40px) saturate(150%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 35px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    .verdict-banner {
        padding: 20px 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    div.stButton > button {
        background: linear-gradient(90deg, #0071e3, #00c6ff) !important;
        border: none !important;
        color: white !important;
        padding: 15px 30px !important;
        font-weight: 700 !important;
        border-radius: 100px !important;
        box-shadow: 0 10px 30px rgba(0, 113, 227, 0.3) !important;
        transition: all 0.3s !important;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 40px rgba(0, 113, 227, 0.6) !important;
    }
    
    div[role="radiogroup"] {
        background: rgba(255,255,255,0.05);
        padding: 5px;
        border-radius: 15px;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# Safe Loader Function
def load_lottie(url):
    try: 
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        return None
    except: 
        return None

# --- 3. FRONT END ---
st.markdown("<h1 class='ultra-title'>Forensic.</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #86868b; font-size: 1.2rem; margin-top:-15px;'>Digital Sports Integrity Framework</p>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="liquid-glass">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        input_type = st.radio("Media Source", ["📁 Upload File", "🔗 Video URL"], horizontal=True, label_visibility="collapsed")
        
        file = None
        video_url = ""
        media_ready = False

        if input_type == "📁 Upload File":
            file = st.file_uploader("", type=["mp4", "mov"])
            if file:
                st.video(file)
                media_ready = True
        else:
            video_url = st.text_input("Paste video link (YouTube, Twitter, public MP4)")
            if video_url:
                try:
                    st.video(video_url)
                    media_ready = True
                except:
                    st.error("Cannot load video preview. Ensure the link is public.")

        if not media_ready:
            # THE FIX: Safely load and check the animation
            anim_waiting = load_lottie("https://assets5.lottiefiles.com/packages/lf20_6p8ovm.json")
            if anim_waiting:
                st_lottie(anim_waiting, height=300)
            else:
                st.info("System Ready. Waiting for encrypted media uplink...")

    with col_right:
        if media_ready:
            if st.button("EXECUTE QUANTUM AUDIT"):
                with st.status("🔮 Analyzing Physics & Metadata...", expanded=True) as s:
                    try:
                        api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyDD4L7TnfAoXiB96P3Gdlki-_KPqtFwWVA")
                        client = genai.Client(api_key=api_key)

                        instruction = """
                        You are a Sports Media Integrity Expert.
                        Analyze the provided media or context for deepfakes and unauthorized redistribution.
                        You MUST end with exactly:
                        FINAL_VERDICT: [AUTHENTIC, MANIPULATED, or UNAUTHORIZED REDISTRIBUTION]
                        CONFIDENCE_SCORE: [Number]%
                        """

                        contents_payload = []
                        if file:
                            with open("temp.mp4", "wb") as f: f.write(file.getbuffer())
                            g_file = client.files.upload(file="temp.mp4")
                            while g_file.state.name == "PROCESSING":
                                time.sleep(2)
                                g_file = client.files.get(name=g_file.name)
                            contents_payload = [g_file, "Is this video authentic or manipulated?"]
                        else:
                            contents_payload = [f"Analyze the context and validity of this video link: {video_url}. Is it a known official broadcast or a known fake/pirated stream?"]

                        response = client.models.generate_content(
                            model="gemini-3.1-pro-preview",
                            config={
                                'system_instruction': instruction,
                                'tools': [{'google_search': {}}]
                            },
                            contents=contents_payload
                        )
                        
                        s.update(label="Audit Complete", state="complete")
                        
                        res_upper = response.text.upper()
                        if "AUTHENTIC" in res_upper: 
                            v_color, v_label, v_icon = "#34c759", "AUTHENTIC", "✅"
                        elif "MANIPULATED" in res_upper: 
                            v_color, v_label, v_icon = "#ff3b30", "SUSPICIOUS (MANIPULATED)", "⚠️"
                        elif "UNAUTHORIZED" in res_upper: 
                            v_color, v_label, v_icon = "#ff9500", "UNAUTHORIZED REDISTRIBUTION", "🏴‍☠️"
                        else: 
                            v_color, v_label, v_icon = "#86868b", "INCONCLUSIVE", "❓"
                        
                        conf_match = re.search(r'CONFIDENCE_SCORE:\s*(\d+)', res_upper)
                        conf = int(conf_match.group(1)) if conf_match else 100

                        st.markdown(f"""
                        <div class="verdict-banner" style="background: {v_color}15; border-left: 6px solid {v_color};">
                            <div>
                                <p style="margin:0; font-size:0.9rem; color:#86868b; font-weight:700;">FINAL VERDICT</p>
                                <h2 style="margin:0; color:{v_color}; font-weight:900;">{v_icon} {v_label}</h2>
                            </div>
                            <div style="text-align:right;">
                                <p style="margin:0; font-size:0.9rem; color:#86868b; font-weight:700;">CONFIDENCE</p>
                                <h2 style="margin:0; color:white; font-weight:900;">{conf}%</h2>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.write(response.text)
                        
                    except Exception as e: st.error(f"Error: {e}")
                    finally: 
                        if file and os.path.exists("temp.mp4"): os.remove("temp.mp4")
        else:
            st.write("### System Status")
            st.markdown("🟢 **Neural Engine:** Active")
            st.markdown("🔵 **Uplink:** Waiting for input...")
            
            # THE FIX: Safely load and check the scanning animation
            anim_status = load_lottie("https://assets10.lottiefiles.com/packages/lf20_st79sc61.json")
            if anim_status:
                st_lottie(anim_status, height=200)
            else:
                st.markdown("📡 *Scanning network frequencies...*")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.1); font-size: 0.8rem; margin-top: 40px;'>IIT BHILAI • GDG SOLUTION CHALLENGE 2026</p>", unsafe_allow_html=True)
