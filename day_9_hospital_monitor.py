import streamlit as st
import random
import time
import threading
import pandas as pd

st.set_page_config(page_title="Multi-Patient Monitoring", layout="wide")
st.title("🏥 Multi-Patient Live Monitoring Dashboard")
st.write("Simulating live sensor data for multiple patients: Heart Rate, Temperature, Oxygen Level")

patients = ["Arun", "Meena", "John", "Priya", "Ravi"]

# Shared dictionary for threads
shared_data = {p: {"hr": 0, "temp": 0, "ox": 0, "alert": ""} for p in patients}

# --- UI placeholders ---
placeholders = {}
for p in patients:
    placeholders[p] = {
        "container": st.container(),
        "hr_bar": None, "temp_bar": None, "ox_bar": None,
        "hr_text": None, "temp_text": None, "ox_text": None, "alert_text": None
    }
    with placeholders[p]["container"]:
        st.subheader(f"Patient: {p}")
        placeholders[p]["hr_bar"] = st.progress(0)
        placeholders[p]["temp_bar"] = st.progress(0)
        placeholders[p]["ox_bar"] = st.progress(0)
        placeholders[p]["hr_text"] = st.empty()
        placeholders[p]["temp_text"] = st.empty()
        placeholders[p]["ox_text"] = st.empty()
        placeholders[p]["alert_text"] = st.empty()

# --- Sensor simulation thread ---
def sensor_thread():
    while True:
        for p in patients:
            shared_data[p]["hr"] = random.randint(60, 110)
            shared_data[p]["temp"] = round(random.uniform(97, 101), 1)
            shared_data[p]["ox"] = random.randint(90, 100)
        time.sleep(1)

# --- Alert detection thread ---
def alert_thread():
    while True:
        for p in patients:
            alert_msg = ""
            if shared_data[p]["hr"] > 100:
                alert_msg += f"⚠️ HR High ({shared_data[p]['hr']} bpm) "
            if shared_data[p]["temp"] > 100:
                alert_msg += f"🌡️ Temp High ({shared_data[p]['temp']} °F) "
            if shared_data[p]["ox"] < 95:
                alert_msg += f"🩸 O2 Low ({shared_data[p]['ox']}%)"
            shared_data[p]["alert"] = alert_msg.strip()
        time.sleep(0.5)

# --- Logging thread ---
def logging_thread():
    while True:
        df = pd.DataFrame([{
            "Patient": p,
            "Heart Rate": shared_data[p]["hr"],
            "Temperature": shared_data[p]["temp"],
            "Oxygen": shared_data[p]["ox"],
            "Alert": shared_data[p]["alert"]
        } for p in patients])
        print("\n--- Latest Patient Logs ---\n", df)
        time.sleep(5)

# Start threads once
if "threads_started" not in st.session_state:
    st.session_state.threads_started = True
    threading.Thread(target=sensor_thread, daemon=True).start()
    threading.Thread(target=alert_thread, daemon=True).start()
    threading.Thread(target=logging_thread, daemon=True).start()

# --- Safe Progress Bar Calculation ---
def safe_progress(value, min_val, max_val):
    """Normalize safely to [0, 1] range for Streamlit progress bar."""
    norm = (value - min_val) / (max_val - min_val)
    return max(0.0, min(1.0, norm))

# --- Main UI update loop ---
while True:
    for p in patients:
        hr = shared_data[p]["hr"]
        temp = shared_data[p]["temp"]
        ox = shared_data[p]["ox"]
        alert_msg = shared_data[p]["alert"]

        # Safe normalization for progress bars
        hr_progress = safe_progress(hr, 60, 110)
        temp_progress = safe_progress(temp, 97, 101)
        ox_progress = safe_progress(ox, 90, 100)

        placeholders[p]["hr_bar"].progress(hr_progress)
        placeholders[p]["temp_bar"].progress(temp_progress)
        placeholders[p]["ox_bar"].progress(ox_progress)

        placeholders[p]["hr_text"].text(f"❤️ Heart Rate: {hr} bpm")
        placeholders[p]["temp_text"].text(f"🌡️ Temperature: {temp} °F")
        placeholders[p]["ox_text"].text(f"🩸 Oxygen Level: {ox}%")

        if alert_msg:
            placeholders[p]["alert_text"].error(alert_msg)
        else:
            placeholders[p]["alert_text"].success("🟢 All readings normal")

    time.sleep(1)