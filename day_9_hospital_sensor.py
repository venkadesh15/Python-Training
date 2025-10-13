import streamlit as st
import random, time, datetime

st.title("🏥 Hospital Patient Sensor Monitor 🩺")
st.write("Simulate patient vital signs and monitor for alerts.")

placeholder = st.empty()
start = st.toggle("Start Monitoring")

if start:
    while True:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        temp = round(random.uniform(95, 104), 1)
        oxy = random.randint(85, 100)
        alert = ""
        if temp < 97 or temp > 100.4: alert += "🌡️ Temp Alert! "
        if oxy < 95: alert += "🩸 Oxygen Alert! "
        with placeholder.container():
            st.metric("⏰ Time", now)
            st.metric("🌡️ Temperature (°F)", temp)
            st.metric("🩸 Oxygen (%)", oxy)
            if alert:
                st.error(alert)
            else:
                st.success("✅ Normal Vitals")
        time.sleep(2)
else:
    st.info("Click toggle to start monitoring.")
