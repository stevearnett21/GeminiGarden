import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types 
from PIL import Image
import time

# --- 1. SECURITY & SYNC ---
if "API_KEY" in st.secrets:
    active_key = st.secrets["API_KEY"]
else:
    active_key = st.sidebar.text_input("🔑 API Key", type="password")

if not active_key:
    st.warning("⚠️ Enter your new Key to wake up Gemini.")
    st.stop()

client = genai.Client(api_key=active_key)

# --- 2. THE DASHBOARD ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")
st.title("🌿 Gemini Garden OS v5.8 (Robust Build)")

tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 AI Vision", "🛡️ Bo's Tasks"])

with tab1:
    gallons = st.number_input("Gallons added:", 0.1, 12.0, 1.0)
    st.info(f"Mix: {(gallons*2.4):.1f}g MB | {(gallons*1.2):.1f}g Epsom | {(gallons*2.4):.1f}g Cal-Nitrate")

with tab2:
    st.header("AI Vision Health Check")
    img_file = st.camera_input("Scan your Garden")
    
    if img_file:
        img = Image.open(img_file)
        with st.spinner("Analyzing (with Tier 1 Fallback)..."):
            # TRY 1: Gemini 2.0 (The flagship)
            try:
                safety = [types.SafetySetting(category=c, threshold="OFF") for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=["Analyze this plant's health.", img],
                    config=types.GenerateContentConfig(safety_settings=safety)
                )
                st.success(response.text)
            
            except Exception as e:
                if "429" in str(e):
                    st.warning("🔄 2.0 Quota Syncing... Falling back to 1.5 Flash.")
                    # TRY 2: Gemini 1.5 (The reliable backup)
                    try:
                        response = client.models.generate_content(
                            model="gemini-1.5-flash", 
                            contents=["Analyze this plant's health.", img]
                        )
                        st.success(response.text)
                    except Exception as e2:
                        st.error(f"Critical Quota Error: {e2}")

with tab3:
    st.header("🛡️ Bo Danger's Garden Quests")
    tasks = st.checkbox("Check water level")
    tasks2 = st.checkbox("Look for yellow leaves")
    tasks3 = st.checkbox("Say hi to the plants")
    if tasks and tasks2 and tasks3:
        st.balloons()
        st.success("Level Up! Bo earned 500 XP!")
