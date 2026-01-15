import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from google import genai # <--- The new 2026 unified import
from PIL import Image

# --- 1. THE NEW 2026 BRAIN: YOUR API KEY ---
API_KEY = "AIzaSyB7AYrYO4baWUVggbWhL_mM5iWI_UOAjMI" 

# Initialize the new Client
client = genai.Client(api_key=API_KEY)

# --- 2. APP CONFIG & STYLE ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .status-card { padding: 15px; border-radius: 10px; background-color: #1c2128; border-left: 5px solid #4CAF50; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'xp' not in st.session_state:
    st.session_state.xp = 0

# --- 4. MAIN DASHBOARD ---
st.title("🌿 Gemini Garden OS v5.0 (Unified Build)")
st.write(f"Independence Mode Active for Steve & Bo Arnett.")

tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 Live Eye & Bo's Game", "📂 System Logs"])

with tab1:
    st.header("Masterblend Mixing Station")
    gallons = st.number_input("Gallons added:", 0.1, 12.0, 1.0)
    st.markdown(f"""
    <div class='status-card'>
    <b>Masterblend:</b> {(gallons * 2.4):.1f}g | 
    <b>Epsom Salt:</b> {(gallons * 1.2):.1f}g | 
    <b>Cal-Nitrate:</b> {(gallons * 2.4):.1f}g
    </div>
    """, unsafe_allow_html=True)
    if st.button("Log Feeding"):
        st.session_state.history.append({"Date": datetime.now().strftime("%Y-%m-%d"), "Type": "Feeding", "Gallons": gallons})

with tab2:
    st.header("AI Vision Portal")
    mode = st.radio("Select Mode:", ["Plant Doctor (Steve)", "Plant ID Game (Bo)"])
    img_file = st.camera_input("Scan the Garden")
    
    if img_file:
        img = Image.open(img_file)
        
        with st.spinner("Gemini is analyzing..."):
            # The prompt based on who is using the app
            if mode == "Plant Doctor (Steve)":
                prompt_text = "Analyze this plant. Check for yellowing, brown tips, or pests for a Rise Garden using Masterblend."
            else:
                prompt_text = "Identify this plant and ask 7-year-old Bo Arnett a fun learning question about it!"
            
            # The new 2026 way to generate content
            response = client.models.generate_content(
                model="gemini-2.0-flash", # Latest 2026 model
                contents=[prompt_text, img]
            )
            
            st.subheader("AI Result:")
            st.write(response.text)
            
            if mode == "Plant ID Game (Bo)":
                st.session_state.xp += 100
                st.balloons()

with tab3:
    st.header("Maintenance & XP")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    st.write("🏆 **Bo's Current XP:**", st.session_state.xp)
