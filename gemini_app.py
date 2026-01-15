import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types 
from PIL import Image

# --- 1. THE BRAIN: SECURITY FIRST ---
# We now look for the key in a sidebar so it doesn't get leaked again!
st.sidebar.title("🔐 Security")
api_key_input = st.sidebar.text_input("Enter New API Key", type="password")

if api_key_input:
    client = genai.Client(api_key=api_key_input)
else:
    st.warning("⚠️ Please enter your new API key in the sidebar to begin.")
    st.stop()

# --- 2. APP CONFIG ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")

# --- 3. MAIN DASHBOARD ---
st.title("🌿 Gemini Garden OS v5.3 (Security Hardened)")

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
        with st.spinner("Analyzing..."):
            try:
                # Keep the safety filters low but valid
                safety_config = [
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE")
                ]

                prompt = "Analyze this plant health." if mode == "Plant Doctor (Steve)" else "Ask Bo a fun plant question!"

                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=[prompt, img],
                    config=types.GenerateContentConfig(safety_settings=safety_config)
                )
                
                st.subheader("AI Insight:")
                st.write(response.text)

            except Exception as e:
                st.error("🛡️ System Refusal. Check if the image contains a clear human face.")
                st.write(f"Reason: {str(e)}")

with tab3:
    st.header("Garden History")
    # ... (History logic remains the same)
