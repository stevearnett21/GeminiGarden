import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types 
from PIL import Image

# --- 1. SECURITY: THE SMART BRAIN ---
# This looks for the key in Secrets first, then the sidebar.
if "API_KEY" in st.secrets:
    active_key = st.secrets["API_KEY"]
else:
    active_key = st.sidebar.text_input("🔑 Enter New API Key", type="password")

if not active_key:
    st.warning("⚠️ No active brain detected. Please enter your NEW API Key in the sidebar.")
    st.stop()

# Initialize Client
client = genai.Client(api_key=active_key)

# --- 2. APP UI ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")
st.title("🌿 Gemini Garden OS v5.6")

tab1, tab2 = st.tabs(["🧪 Nutrient Lab", "📸 AI Vision Portal"])

with tab1:
    st.header("Masterblend Calculator")
    gallons = st.number_input("Gallons added:", 0.1, 12.0, 1.0)
    st.info(f"Mix: {(gallons*2.4):.1f}g MB | {(gallons*1.2):.1f}g Epsom | {(gallons*2.4):.1f}g Cal-Nitrate")

with tab2:
    st.header("AI Vision Health Check")
    img_file = st.camera_input("Scan your Garden")
    
    if img_file:
        img = Image.open(img_file)
        with st.spinner("Analyzing with fresh API Key..."):
            try:
                # 🛠️ THE 2026 "OFF" SAFETY FIX
                safety_config = [
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF")
                ]

                prompt = "Analyze this plant's health. Ignore the purple LED lighting and shadows."

                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=[prompt, img],
                    config=types.GenerateContentConfig(safety_settings=safety_config)
                )
                
                st.subheader("AI Insight:")
                st.success(response.text)

            except Exception as e:
                # This will tell us if it's a LEAK error or a LIGHTING error
                st.error("🛡️ System Error")
                st.code(str(e))
