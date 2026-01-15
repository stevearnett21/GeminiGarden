import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types 
from PIL import Image

# --- 1. THE BRAIN: SECURITY & DISCOVERY ---
if "API_KEY" in st.secrets:
    active_key = st.secrets["API_KEY"]
else:
    active_key = st.sidebar.text_input("🔑 API Key", type="password")

if not active_key:
    st.warning("⚠️ Enter your key in the sidebar.")
    st.stop()

client = genai.Client(api_key=active_key)

# DEBUG: Print all available models to your CMD window once
if 'models_checked' not in st.session_state:
    print("--- 🔎 DISCOVERING AVAILABLE MODELS FOR STEVE ---")
    for m in client.models.list():
        print(f"Model ID: {m.name}")
    st.session_state.models_checked = True

# --- 2. APP CONFIG ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")
st.title("🌿 Gemini Garden OS v6.0 (Unified)")

tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 AI Vision", "📊 Bo's XP & Logs"])

with tab2:
    st.header("AI Vision Health Check")
    img_file = st.camera_input("Scan your Garden")
    
    if img_file:
        img = Image.open(img_file)
        with st.spinner("Handshaking with Gemini..."):
            try:
                # 🛠️ THE 2026 GLOBAL STABLE ALIASES
                # 'gemini-2.0-flash' or 'gemini-1.5-flash' are now the standard
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=["Analyze this plant's health. Ignore LED glare.", img],
                    config=types.GenerateContentConfig(
                        safety_settings=[types.SafetySetting(category=c, threshold="OFF") 
                                       for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                                 "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
                    )
                )
                st.success(response.text)
            
            except Exception as e:
                # FALLBACK to the simplest possible alias if 2.0 fails
                st.warning("🔄 Attempting Global Stable Fallback...")
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash", # No version numbers, just the stable alias
                        contents=["Analyze this plant's health.", img]
                    )
                    st.success(response.text)
                except Exception as e2:
                    st.error(f"Handshake Failed: {e2}")
