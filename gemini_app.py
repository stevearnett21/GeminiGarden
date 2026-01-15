import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai 
from google.genai import types 
from PIL import Image

# --- 1. SECURITY & BRAIN ---
# This looks for your API Key in Streamlit's "Secrets" storage (Cloud) 
# or a local file (Local). This keeps it off the screen!
if "API_KEY" in st.secrets:
    API_KEY = st.secrets["API_KEY"]
else:
    # If no secret is found, show a password box in the sidebar
    API_KEY = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not API_KEY:
    st.warning("🔐 Please enter your API Key in the sidebar or set it in Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- 2. APP UI ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿")
st.title("🌿 Gemini Garden OS v5.3")

# --- 3. THE TABS ---
tab1, tab2, tab3 = st.tabs(["🧪 Nutrients", "📸 AI Vision", "📂 History"])

with tab1:
    st.header("Masterblend Calculator")
    gallons = st.number_input("Gallons added:", 0.1, 12.0, 1.0)
    st.info(f"Mix: {(gallons*2.4):.1f}g MB | {(gallons*1.2):.1f}g Epsom | {(gallons*2.4):.1f}g Cal-Nitrate")

with tab2:
    st.header("Bo's AI Game & Doctor Mode")
    mode = st.radio("Mode:", ["Doctor", "Bo's Game"])
    img_file = st.camera_input("Scan")
    
    if img_file:
        img = Image.open(img_file)
        with st.spinner("Analyzing..."):
            try:
                # 2026 Safety Bypass Logic
                safety = [types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                          types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                          types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                          types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE")]

                prompt = "Check plant health." if mode == "Doctor" else "Ask 7-year-old Bo a fun plant question!"
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=[prompt, img],
                    config=types.GenerateContentConfig(safety_settings=safety)
                )
                st.write(response.text)
            except Exception as e:
                st.error("🛡️ Safety Filter Triggered. Try a different angle or brighter light!")

with tab3:
    st.header("System Logs")
    st.write("XP: 0") # Placeholder
