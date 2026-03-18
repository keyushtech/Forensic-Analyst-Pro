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

# --- 1. SETTINGS & SECRETS ---
st.set_page_config(page_title="Forensic Pro", layout="wide", initial_sidebar_state="collapsed")

def load_lottie(url):
    try:
        return requests.get(url).json()
    except: return None

# High-end Lottie Animations
LOTTIE_SCAN = "https://lottie.host/86828591-0309-4393-9791-236f0607c376/XyZlJAn323.json"
LOTTIE_DASH = "https://lottie.host/5a914436-b52b-4228-8798-5a41a4a44b82/7ZqH4X8Y2k.json"

# --- 2. THE LIQUID GLASS ENGINE (CSS) ---
st.markdown("""
    <style>
    /* Animated Liquid Background */
    .stApp {
        background: linear-gradient(120deg, #000000, #1a1a1a, #001f3f);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 2rem;
    }

    /* Floating Animation for Cards */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .floating-card { animation: float 6s ease-in-out infinite; }

    /* Apple-style Gradient Text */
    .shimmer-text {
        background: linear-gradient(90deg, #ffffff, #86868b, #ffffff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 5s linear infinite;
        font-weight: 800;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Button Styling */
    div.stButton > button {
        background: rgba(0, 113, 227, 0.8) !important;
        backdrop-filter: blur(10px);
        border-radius: 980px !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div.stButton > button:hover {
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 113, 227, 0.4);
        background: rgba(0, 113, 227, 1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. UI LAYOUT ---
st.markdown("<h1 class='shimmer-text' style='text-align:center;'>Forensic Analysis Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#86868b; margin-top:-20px;'>Digital Sports Media Integrity Framework</p>", unsafe_allow_html=True)

main_col_l, main_col_center, main_col_r = st.columns([0.1, 1, 0.1])

with main_col_center:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    col_input, col_report = st.columns([1, 1.2], gap="large")
    
    with col_input:
        uploaded_file = st.file_uploader("", type=["mp4", "mov"])
        if uploaded_file:
            st.video(uploaded_file)
        else:
            anim_data = load_lottie(LOTTIE_DASH)
            if anim_data: st_lottie(anim_data, height=300)

    with col_report:
        if uploaded_file:
            if st.button("Initialize Deep Audit"):
                temp_path = "temp_video.mp4"
                with open(temp_path, "wb") as f: f.write(uploaded_file.getbuffer())
                
                with st.status("🔬 Quantum Pixel Inspection...", expanded=True) as status:
                    try:
                        # API Setup
                        api_key = st.secrets.get("GEMINI_API_KEY", "PASTE_NEW_KEY_HERE")
                        client = genai.Client(api_key=api_key)
                        
                        # Process
                        gemini_file = client.files.upload(file=temp_path)
                        while gemini_file.state.name == "PROCESSING":
                            time.sleep(2)
                            gemini_file = client.files.get(name=gemini_file.name)
                        
                        response = client.models.generate_content(
                            model="gemini-3.1-pro-preview",
                            contents=[gemini_file, "Is this video authentic or manipulated? Focus on redistribution marks."]
                        )
                        
                        # Parsing logic (using your established regex)
                        res_text = response.text.upper()
                        v_label = "Authentic" if "AUTHENTIC" in res_text else "Manipulated"
                        v_color = "#34c759" if v_label == "Authentic" else "#ff3b30"
                        
                        status.update(label="Audit Complete", state="complete")
                        
                        # Results UI
                        st.markdown(f"### Result: <span style='color:{v_color}'>{v_label}</span>", unsafe_allow_html=True)
                        st.write(response.text)
                        
                        if v_label == "Manipulated":
                            st.error("Deepfake Artifacts Detected.")
                        
                    except Exception as e: st.error(f"Error: {e}")
                    finally: 
                        if os.path.exists(temp_path): os.remove(temp_path)
        else:
            st.info("Upload a sports clip to begin the integrity audit.")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align:center; color:#424245; font-size:0.8rem;'>IIT Bhilai • Built for GDG Solution Challenge 2026</p>", unsafe_allow_html=True)
