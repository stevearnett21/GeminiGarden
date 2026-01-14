import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import google.generativeai as genai
from PIL import Image

# --- 1. THE BRAIN: YOUR API KEY ---
# I have put your specific key here so it works immediately!
API_KEY = "AIzaSyB7AYrYO4baWUVggbWhL_mM5iWI_UOAjMI" 
genai.configure(api_key=API_KEY)

# --- 2. APP CONFIG & STYLE ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .status-card { padding: 15px; border-radius: 10px; background-color: #1c2128; border-left: 5px solid #4CAF50; margin-bottom: 20px; }
    .bo-game { background-color: #2e3b4e; padding: 20px; border-radius: 15px; border: 2px dashed #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE (Persistence) ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'xp' not in st.session_state:
    st.session_state.xp = 0

# --- 4. MAIN DASHBOARD ---
st.title("🌿 Gemini Garden OS v4.0")
st.write(f"Hello Steve! Dashboard active for the St. Peters 2-Level Rise.")

tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 Live Eye & Bo's Game", "📂 System Logs"])

# --- TAB 1: NUTRIENT LAB ---
with tab1:
    st.header("Masterblend Mixing Station")
    gallons = st.number_input("Gallons of water added:", 0.1, 12.0, 1.0)
    
    st.markdown(f"""
    <div class='status-card'>
    <b>Masterblend (4-18-38):</b> {(gallons * 2.4):.1f}g<br>
    <b>Epsom Salt:</b> {(gallons * 1.2):.1f}g<br>
    <b>Calcium Nitrate:</b> {(gallons * 2.4):.1f}g <br>
    <i>Order: Mix MB, then Epsom, then Calcium Nitrate ALWAYS LAST.</i>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Log this Feeding"):
        st.session_state.history.append({"Date": datetime.now().strftime("%Y-%m-%d"), "Type": "Feeding", "Gallons": gallons})
        st.success("Feeding logged!")

# --- TAB 2: LIVE EYE AI ---
with tab2:
    st.header("Real-Time AI Vision")
    mode = st.radio("Select Mode:", ["Plant Doctor (Steve)", "Plant ID Game (Bo)"])
    
    img_file = st.camera_input("Scan the Garden")
    
    if img_file:
        img = Image.open(img_file)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        with st.spinner("Gemini is analyzing the photo..."):
            if mode == "Plant Doctor (Steve)":
                prompt = "Analyze this hydroponic plant. Check for yellowing, brown tips (nutrient burn), or pests. Give advice specifically for a Rise Garden using Masterblend."
            else:
                prompt = "Identify this plant and ask a 7-year-old named Bo a fun question about it to help him learn. Be encouraging!"
            
            response = model.generate_content([prompt, img])
            
            st.subheader("AI Analysis Result:")
            st.write(response.text)
            
            if mode == "Plant ID Game (Bo)":
                st.session_state.xp += 100
                st.balloons()
                st.write(f"✨ **Bo earned 100 XP!** Total XP: {st.session_state.xp}")

# --- TAB 3: SYSTEM LOGS ---
with tab3:
    st.header("Garden History")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    else:
        st.write("No logs yet. Start by logging a feeding!")
    
    st.divider()
    st.write("🏆 **Bo's Current XP:**", st.session_state.xp)
