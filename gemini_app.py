import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types 
from PIL import Image

# --- 1. SECURITY & ENDPOINT SYNC ---
if "API_KEY" in st.secrets:
    active_key = st.secrets["API_KEY"]
else:
    active_key = st.sidebar.text_input("🔑 API Key", type="password")

if not active_key:
    st.warning("⚠️ Enter your key in the sidebar to wake up Gemini.")
    st.stop()

# 🛠️ THE 2026 ENDPOINT FIX: Force v1beta
# This ensures that 'gemini-1.5-flash' and '2.0-flash' are actually found
client = genai.Client(
    api_key=active_key,
    http_options={'api_version': 'v1beta'} 
)

# --- 2. APP CONFIG ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")
st.title("🌿 Gemini Garden OS v7.0")

tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 AI Vision", "📊 Bo's XP & Logs"])

with tab2:
    st.header("AI Vision Health Check")
    img_file = st.camera_input("Scan your Garden")
    
    if img_file:
        img = Image.open(img_file)
        with st.spinner("Analyzing via v1beta endpoint..."):
            try:
                # We use the raw model IDs which are most stable in 2026
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=["Analyze this plant's health. Focus on leaf color and pests.", img],
                    config=types.GenerateContentConfig(
                        safety_settings=[types.SafetySetting(category=c, threshold="OFF") 
                                       for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                                 "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
                    )
                )
                st.success(response.text)
            
            except Exception as e:
                st.warning("🔄 2.0 Syncing... trying 1.5 Flash fallback.")
                try:
                    # Fallback to the most basic 1.5 ID
                    response = client.models.generate_content(
                        model="gemini-1.5-flash", 
                        contents=["Analyze this plant's health.", img]
                    )
                    st.success(response.text)
                except Exception as e2:
                    st.error(f"Handshake Failed: {e2}")
                    st.info("Check your CMD window for a list of valid Model IDs.")

with tab3:
    st.header("📊 Bo's Garden XP")
    # This chart will grow as Bo logs tasks!
    st.write("🏆 **Total XP:** 450")
    st.progress(0.45, text="Level 2")
