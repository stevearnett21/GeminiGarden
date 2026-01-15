import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from google import genai  # The 2026 Unified SDK
from PIL import Image

# --- 1. THE BRAIN: YOUR API KEY ---
# Replace with your key: AIzaSyB7AYrYO4baWUVggbWhL_mM5iWI_UOAjMI
API_KEY = "AIzaSyB7AYrYO4baWUVggbWhL_mM5iWI_UOAjMI" 
client = genai.Client(api_key=API_KEY)

# --- 2. APP CONFIG & STYLE ---
st.set_page_config(page_title="Gemini Garden OS", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .status-card { padding: 15px; border-radius: 10px; background-color: #1c2128; border-left: 5px solid #4CAF50; margin-bottom: 20px; }
    .stButton>button { border-radius: 20px; width: 100%; height: 3em; background-color: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'xp' not in st.session_state:
    st.session_state.xp = 0

# --- 4. MAIN DASHBOARD ---
st.title("🌿 Gemini Garden OS v5.1")
st.write(f"St. Peters Unit | System Independent of Rise Cloud")

tab1, tab2, tab3 = st.tabs(["🧪 Nutrient Lab", "📸 Live Eye & Bo's Game", "📂 System Logs"])

with tab1:
    st.header("Masterblend Mixing Station")
    gallons = st.number_input("How many gallons are you adding?", 0.1, 12.0, 1.0)
    
    st.markdown(f"""
    <div class='status-card'>
    <b>Masterblend (4-18-38):</b> {(gallons * 2.4):.1f}g<br>
    <b>Epsom Salt:</b> {(gallons * 1.2):.1f}g<br>
    <b>Cal-Nitrate:</b> {(gallons * 2.4):.1f}g <br>
    <small>Order: Dissolve MB, then Epsom, then Cal-Nitrate LAST.</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Log Full Feed & Save Progress"):
        st.session_state.history.append({"Date": datetime.now().strftime("%Y-%m-%d"), "Type": "Feed", "Gallons": gallons})
        st.success("Feeding logged to the Man Cave server!")

with tab2:
    st.header("AI Vision & Bo's Identification Game")
    mode = st.radio("Select User:", ["Plant Doctor (Steve)", "Plant ID Game (Bo)"])
    
    img_file = st.camera_input("Point at your Garden")
    
    if img_file:
        img = Image.open(img_file)
        
        with st.spinner("Gemini 2.0-Flash is analyzing..."):
            try:
                # Set prompts for 2026 model logic
                if mode == "Plant Doctor (Steve)":
                    prompt = "Analyze this plant. If it's a person, politely ask to see a plant instead. Check for nutrient burn or pests for a Rise Garden."
                else:
                    prompt = "Identify this plant and ask Bo Arnett (7 years old) a fun science question about it! Be encouraging."

                # The new 2026 Unified Call
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=[prompt, img]
                )
                
                st.subheader("AI Insight:")
                st.write(response.text)
                
                if mode == "Plant ID Game (Bo)":
                    st.session_state.xp += 100
                    st.balloons()

            except Exception as e:
                # Catching the Face Safety Filter
                st.error("🛡️ **Safety Shield:** Gemini cannot analyze human faces. Please point the camera at your plants!")

with tab3:
    st.header("Garden Archives")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history))
    st.write("🏆 **Bo's Current Garden XP:**", st.session_state.xp)

st.divider()
st.caption("Powered by Gemini 2.0 Unified SDK | St. Peters, MO | 2026")
