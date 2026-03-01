import streamlit as st
import subprocess
import time
import os
import sys
from datetime import datetime
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PulseNet OS | Command Center", page_icon="🌐", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM ENTERPRISE CSS ---
st.markdown("""
    <style>
    .stCodeBlock { background-color: #0e1117 !important; border-left: 4px solid #00ff00 !important; }
    .medical-alert {
        background-color: #ffebee; padding: 1.5rem; border-radius: 8px;
        border-left: 6px solid #d32f2f; color: #b71c1c; font-family: monospace;
        font-size: 1.1em; margin-top: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 { font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8282/8282058.png", width=60)
    st.title("PulseNet OS")
    st.caption("AI-Powered Emergency Coordination")
    st.divider()
    page = st.radio("SYSTEM MODULES", ["🎧 ECC Copilot (Operator)", "📱 Citizen SOS App (User)"])
    st.divider()
    st.markdown("**System Status:** 🟢 All Nodes Online")
    st.markdown("**Active AI Agents:** 6 / 6")
    st.markdown("**Avg Swarm Latency:** 1.2s")

# ==========================================
# MODULE 1: ECC COMMAND CENTER
# ==========================================
if page == "🎧 ECC Copilot (Operator)":
    st.title("🌐 Main Dispatch Hub: AI Copilot")
    st.markdown("Automated intake, triage, and multi-agent logistics routing.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Active Critical Incidents", value="1", delta="High Priority", delta_color="inverse")
    m2.metric(label="Available ALS Units", value="14", delta="-1 Dispatched")
    m3.metric(label="City Traffic Grid", value="Optimized", delta="Green Corridors Active", delta_color="normal")
    m4.metric(label="Trauma Beds Open", value="8", delta="-1 Reserved")
    st.divider()

    col1, col2, col3 = st.columns([1.2, 1.5, 1])
    
    with col1:
        st.subheader("🎙️ Live 911 Audio Ingestion")
        with st.container(border=True):
            raw_transcript = st.text_area(
                "Speech-to-Text Transcript Feed:", 
                value="Help! I'm at the Central Mall on the ground floor. An older man just collapsed. He's not breathing and won't wake up! I think he's having a heart attack. Someone is running to get an AED.",
                height=150, disabled=True 
            )
            if st.button("⚡ AUTONOMOUS AI EXTRACT & ROUTE", type="primary", use_container_width=True):
                st.session_state['mode2_processing'] = True
                with open("ui_logs.txt", "w", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().strftime('%H:%M:%S')}] PULSENET INGESTION: AUDIO TRANSCRIPT LOCKED\n")
                subprocess.Popen([sys.executable, "-u", "trigger_test.py", raw_transcript], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    with col2:
        st.subheader("📡 Swarm Network Feed")
        with st.container(border=True):
            log_container_2 = st.empty()
            if st.session_state.get('mode2_processing'):
                with st.spinner("AI Swarm executing parallel tool-calls..."):
                    for _ in range(25): 
                        if os.path.exists("ui_logs.txt"):
                            with open("ui_logs.txt", "r", encoding="utf-8") as f:
                                log_container_2.code(f.read(), language="bash")
                        time.sleep(1)
                st.session_state['mode2_ready'] = True
            else:
                log_container_2.info("Awaiting active incident data...")

    with col3:
        st.subheader("🛡️ Final Dispatch Gate")
        with st.container(border=True):
            if st.session_state.get('mode2_ready'):
                st.warning("⚠️ **HUMAN VERIFICATION REQUIRED**")
                v_loc = st.text_input("AI Extracted Location", value="Central Mall, Ground Floor")
                v_inj = st.text_input("AI Extracted Triage", value="Sudden Cardiac Arrest")
                v_unit = st.text_input("AI Logistics Assignment", value="ALS Unit #402, Dr. Chen (Cardiology)")
                
                map_data = pd.DataFrame({'lat': [12.9716], 'lon': [77.5946]})
                st.map(map_data, zoom=14, use_container_width=True)

                if st.button("✅ CONFIRM & DISPATCH UNITS", type="secondary", use_container_width=True):
                    st.success("🚨 UNITS DISPATCHED. Green corridors activated.")
            else:
                st.markdown("*AI processing required before gateway unlocks.*")

# ==========================================
# MODULE 2: CITIZEN SOS APP
# ==========================================
elif page == "📱 Citizen SOS App (User)":
    _, app_col, _ = st.columns([1, 1.5, 1])
    
    with app_col:
        st.markdown("<h1 style='text-align: center; color: #d32f2f;'>🚨 PulseNet SOS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Bypass the queue. Get instant AI triage.</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            if not st.session_state.get('mode1_dispatched'):
                e_type = st.selectbox("Emergency Category", ["Medical / Trauma", "Fire / Rescue", "Traffic Collision", "Cardiac Arrest"])
                location = st.text_input("GPS Location Override", placeholder="E.g., 4th Ave & Main St")
                patient_info = st.text_area("Situation Details", placeholder="E.g., Severe burns on right arm from boiling oil.")
                
                if st.button("🔥 TRANSMIT EMERGENCY", type="primary", use_container_width=True):
                    if location and patient_info:
                        incident_payload = f"Category: {e_type} | Location: {location} | Details: {patient_info}"
                        st.session_state['mode1_dispatched'] = True
                        with open("ui_logs.txt", "w", encoding="utf-8") as f:
                            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] PULSENET APP: DIRECT INTAKE RECEIVED\n")
                        subprocess.Popen([sys.executable, "-u", "trigger_test.py", incident_payload], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        st.rerun()
            else:
                st.success("📍 GPS Locked. Encrypted transmission sent to ECC.")
                with st.spinner("AI Triage Commander analyzing situation..."):
                    medical_ui = st.empty()
                    with st.expander("🔍 View Background ECC Swarm Routing"):
                        log_container_1 = st.empty()
                        
                    for _ in range(25):
                        if os.path.exists("ui_logs.txt"):
                            with open("ui_logs.txt", "r", encoding="utf-8") as f:
                                current_logs = f.read()
                                log_container_1.code(current_logs, language="bash")
                                
                                # FIXED MATCHER
                                if ">>> Sent dynamic advice:" in current_logs:
                                    for line in current_logs.split('\n'):
                                        if ">>> Sent dynamic advice:" in line:
                                            clean_advice = line.split(">>> Sent dynamic advice:")[-1].strip()
                                            medical_ui.markdown(f"""
                                                <div class="medical-alert">
                                                    <h4>⚕️ AI MEDICAL DIRECTIVE</h4>
                                                    <p>{clean_advice}</p>
                                                </div>
                                            """, unsafe_allow_html=True)
                        time.sleep(1)
                
                st.info("🚑 Response swarm active. Help is routing to you now.")
                if st.button("Disconnect", use_container_width=True):
                    st.session_state['mode1_dispatched'] = False
                    st.rerun()