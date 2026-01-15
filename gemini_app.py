import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types 
from PIL import Image

# --- 1. THE BRAIN: TIER 1 SECURE HANDSHAKE ---
# This ensures we use the correct 2026 endpoint for your new key
if "API_KEY" in st.secrets:
    active_key = st.secrets["API_KEY"]
else:
    active_key = st.sidebar.text_input("🔑 API Key", type="password")

if not active_key:
    st.warning("⚠️ Enter your key in the sidebar to wake up Gemini.")
    st.stop()

# FORCE V1BETA ENDPOINT
client = genai.Client(api_key=active_key, http_options={'api_version': 'v1beta'})

# --- 2. APP UI & STYLE ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")
st.title("🌿 Gemini Garden OS v7.2")

# --- 3. THE TABS ---
# We define three containers here
tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 AI Vision", "📊 Bo's XP & Logs"])

# TAB 1: NUTRIENT LAB (The Masterblend Calculator)
with tab1: # <--- Everything indented under here stays in Tab 1
    st.header("Masterblend Mixing Station")
    st.write("Steve, use these ratios for the 2-Level Rise Garden.")
    
    gallons = st.number_input("Gallons of water added:", 0.1, 12.0, 1.0)
    
    # Industrial Hydroponics Logic
    mb = gallons * 2.4
    epsom = gallons * 1.2
    cal_nitrate = gallons * 2.4
    
    st.markdown(f"""
    <div style="background-color: #1c2128; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;">
        <h3 style="color: #4CAF50; margin-top: 0;">Mixing Recipe:</h3>
        <p>1. <b>Masterblend (4-18-38):</b> {mb:.1f}g</p>
        <p>2. <b>Epsom Salt:</b> {epsom:.1f}g</p>
        <p>3. <b>Calcium Nitrate:</b> {cal_nitrate:.1f}g (Always Last)</p>
        <hr>
        <p><small><i>Total weight: {mb+epsom+cal_nitrate:.1f}g of nutrients per {gallons}gal</i></small></p>
    </div>
    """, unsafe_allow_html=True)

# TAB 2: AI VISION (The Garden Doctor)
with tab2:
    st.header("AI Vision Health Check")
    img_file = st.camera_input("Point at your Garden (Pixel 10)")
    
    if img_file:
        img = Image.open(img_file)
        with st.spinner("Analyzing via v1beta endpoint..."):
            try:
                # SAFETY OFF for Grow Lights
                safety = [types.SafetySetting(category=c, threshold="OFF") 
                          for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                    "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=["Analyze this plant's health. Focus on leaf color and pests.", img],
                    config=types.GenerateContentConfig(safety_settings=safety)
                )
                st.success(response.text)
            except Exception as e:
                st.error(f"AI Handshake Failed: {e}")

# TAB 3: LOGS & XP
with tab3:
    st.header("📊 Bo Danger's Progress")
    st.write("🏆 **Total Garden XP:** 550")
    st.progress(0.55, text="Level 2 Gardener")
    st.info("Don't forget: Masterblend is better than pod-only systems! (Just like Triscuits > Cheez-Its)")
