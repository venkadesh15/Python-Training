import streamlit as st
import pandas as pd
import random
import time
import threading
import altair as alt

REFRESH_EVERY_SECONDS = 2

st.set_page_config(page_title="Hospital Monitoring System", layout="wide")
st.title("🏥 Hospital Monitoring System")
st.write("Live simulation with three concurrent threads: Sensor, Doctor Notification, Data Logging")

# ------------------ SHARED DATA (thread-safe) ------------------
shared = {
    "data": pd.DataFrame(columns=["Time", "Heart Rate", "Temperature", "Blood Pressure"]),
    "alert": "",
    "run": False
}

# ------------------ BUTTONS ------------------
col1, col2 = st.columns(2)
if col1.button("▶️ Start Monitoring"):
    shared["run"] = True
if col2.button("⏹️ Stop Monitoring"):
    shared["run"] = False

# ------------------ THREAD FUNCTIONS ------------------
def sensor_thread():
    while shared["run"]:
        t = time.strftime("%H:%M:%S")
        hr = random.randint(60, 110)
        temp = round(random.uniform(36.0, 39.0), 1)
        bp = random.randint(110, 140)
        new = pd.DataFrame([[t, hr, temp, bp]], columns=["Time", "Heart Rate", "Temperature", "Blood Pressure"])
        shared["data"] = pd.concat([shared["data"], new]).tail(30)
        time.sleep(REFRESH_EVERY_SECONDS)

def doctor_notification_thread():
    while shared["run"]:
        if not shared["data"].empty:
            latest = shared["data"].iloc[-1]
            if latest["Heart Rate"] > 100 or latest["Temperature"] > 38.5 or latest["Blood Pressure"] > 135:
                shared["alert"] = f"⚠️ Critical! HR={latest['Heart Rate']}, Temp={latest['Temperature']}, BP={latest['Blood Pressure']}"
            else:
                shared["alert"] = ""
        time.sleep(1)

def data_logging_thread():
    while shared["run"]:
        if not shared["data"].empty:
            print(f"[Data Log] {shared['data'].tail(1).to_dict('records')[0]}")
        time.sleep(REFRESH_EVERY_SECONDS * 2)

# ------------------ START THREADS ------------------
if "threads_started" not in st.session_state:
    st.session_state.threads_started = False

if shared["run"] and not st.session_state.threads_started:
    st.session_state.threads_started = True
    threading.Thread(target=sensor_thread, daemon=True).start()
    threading.Thread(target=doctor_notification_thread, daemon=True).start()
    threading.Thread(target=data_logging_thread, daemon=True).start()

# ------------------ DISPLAY ------------------
if not shared["data"].empty:
    latest = shared["data"].iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("💓 Heart Rate (bpm)", latest["Heart Rate"])
    c2.metric("🌡️ Temperature (°C)", latest["Temperature"])
    c3.metric("🩸 Blood Pressure (mmHg)", latest["Blood Pressure"])

    df_melt = shared["data"].melt("Time", var_name="Sensor", value_name="Value")
    chart = (
        alt.Chart(df_melt)
        .mark_line(point=True)
        .encode(
            x=alt.X("Time", sort=None, axis=alt.Axis(labelAngle=-45)),
            y="Value",
            color="Sensor",
            strokeWidth=alt.value(3)
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)

# Display alert
if shared["alert"]:
    st.error(shared["alert"])
else:
    st.success("🟢 Monitoring live... all readings normal.")

# ------------------ AUTO REFRESH ------------------
placeholder = st.empty()
time.sleep(REFRESH_EVERY_SECONDS)
placeholder.empty()  # triggers rerun without errors
