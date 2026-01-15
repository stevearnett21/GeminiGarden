import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types 
from PIL import Image

# --- 1. SECURITY & SYNC ---
if "API_KEY" in st.secrets:
    active_key = st.secrets["API_KEY"]
else:
    active_key = st.sidebar.text_input("🔑 API Key", type="password")

if not active_key:
    st.warning("⚠️ Enter your key in the sidebar to wake up Gemini.")
    st.stop()

client = genai.Client(api_key=active_key)

# --- 2. THE DASHBOARD ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")
st.title("🌿 Gemini Garden OS v5.9")

tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 AI Vision", "📊 Bo's XP & Logs"])

with tab1:
    gallons = st.number_input("Gallons added:", 0.1, 12.0, 1.0)
    st.info(f"Mix: {(gallons*2.4):.1f}g MB | {(gallons*1.2):.1f}g Epsom | {(gallons*2.4):.1f}g Cal-Nitrate")

with tab2:
    st.header("AI Vision Health Check")
    img_file = st.camera_input("Scan your Garden")
    
    if img_file:
        img = Image.open(img_file)
        with st.spinner("Analyzing (Unified Fallback active)..."):
            # 🛠️ THE 2026 NAMING FIX
            # Try 2.0 first, then fallback to the verified 1.5 stable name
            try:
                safety = [types.SafetySetting(category=c, threshold="OFF") for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
                
                # We use the specific 2026 stable name here
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=["Analyze this plant's health.", img],
                    config=types.GenerateContentConfig(safety_settings=safety)
                )
                st.success(response.text)
            
            except Exception as e:
                # If 2.0 is still syncing, we use the specific 1.5 stable alias
                st.warning("🔄 2.0 still syncing... attempting verified 1.5 Flash.")
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash-002", # The verified stable name
                        contents=["Analyze this plant's health.", img]
                    )
                    st.success(response.text)
                except Exception as e2:
                    st.error(f"System Error: {e2}")

with tab3:
    st.header("📊 Bo's Garden XP & System Logs")
    # A simple chart to show 'XP progress' over the week
    chart_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'XP': [50, 150, 200, 450, 0, 0, 0] # Example data
    })
    st.line_chart(chart_data.set_index('Day'))
    st.write("🏆 **Bo's Current XP:** 450 / 1000 (Level 2 Gardener)")
