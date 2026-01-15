import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types  # Needed for safety settings
from PIL import Image

# --- 1. THE BRAIN: YOUR API KEY ---
API_KEY = "AIzaSyB7AYrYO4baWUVggbWhL_mM5iWI_UOAjMI" 
client = genai.Client(api_key=API_KEY)

# --- 2. APP CONFIG ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")

# --- 3. SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'xp' not in st.session_state:
    st.session_state.xp = 0

# --- 4. MAIN DASHBOARD ---
st.title("🌿 Gemini Garden OS v5.2 (Safety Fix)")

tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 Live Eye & Bo's Game", "📂 System Logs"])

with tab1:
    st.header("Masterblend Calculator")
    gallons = st.number_input("Gallons added:", 0.1, 12.0, 1.0)
    st.info(f"Add: {(gallons * 2.4):.1f}g MB | {(gallons * 1.2):.1f}g Epsom | {(gallons * 2.4):.1f}g Cal-Nitrate")

with tab2:
    st.header("AI Vision Portal")
    mode = st.radio("Select User:", ["Plant Doctor (Steve)", "Plant ID Game (Bo)"])
    img_file = st.camera_input("Scan the Garden")
    
    if img_file:
        img = Image.open(img_file)
        with st.spinner("Analyzing without filters..."):
            try:
                # Configure the "Unfiltered" Settings for 2026
                safety_config = [
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_CIVIC_INTEGRITY", threshold="BLOCK_NONE"),
                ]

                prompt = "Analyze this plant. If it's a person, say hello. Focus on plant health check for a Rise Garden." if mode == "Plant Doctor (Steve)" else "Identify this plant and ask 7-year-old Bo a fun question!"

                # The 2026 Unified Call with Safety Config
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=[prompt, img],
                    config=types.GenerateContentConfig(safety_settings=safety_config)
                )
                
                st.subheader("AI Insight:")
                st.write(response.text)
                
                if mode == "Plant ID Game (Bo)":
                    st.session_state.xp += 100
                    st.balloons()

            except Exception as e:
                # Detailed error logging for Steve the IT pro
                st.error("🛡️ **System Refusal:** Gemini's internal core safety blocked this image.")
                st.write(f"Technical Reason: {str(e)}")

with tab3:
    st.header("Garden History")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    st.write("🏆 **Bo's Current Garden XP:**", st.session_state.xp)
