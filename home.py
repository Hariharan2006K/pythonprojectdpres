import streamlit as st
import time
import requests

st.title("Disaster Preparedness & Response System")
st.subheader("Basecamp Overview")

st.markdown("""
The Disaster Preparedness and Response Education System (DPRES) is a structured platform designed to train communities and institutions on effective emergency response protocols. 

Use the navigation pane to review survival procedures, test your situational awareness, and monitor institutional readiness metrics.
""")

st.markdown("---")

st.markdown("### 🌦️ Live Environmental Telemetry")
st.write("Monitor real-time weather conditions utilizing the Open-Meteo telemetry framework.")
city = st.text_input("Enter your city to check live weather data", "New York")

if city:
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    try:
        geo_resp = requests.get(geocode_url).json()
        if "results" in geo_resp and len(geo_resp["results"]) > 0:
            lat = geo_resp["results"][0]["latitude"]
            lon = geo_resp["results"][0]["longitude"]
            
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_resp = requests.get(weather_url).json()
            
            if "current_weather" in weather_resp:
                cw = weather_resp["current_weather"]
                st.info(f"**Current conditions in {city.title()}:** {cw['temperature']}°C | Wind Speed: {cw['windspeed']} km/h")
        else:
            st.error(f"Could not locate '{city}'. Please verify the spelling.")
    except Exception as e:
        st.error("Failed to retrieve weather metrics at this time. Telemetry link down.")

st.markdown("---")
st.markdown("### Emergency Alert Simulation")
st.write("Initiate a test of the emergency broadcast system to preview the visual warning parameters.")

if st.button("Simulate Emergency Protocol", type="primary"):
    st.toast("SYSTEM OVERRIDE: Emergency protocols activated. Seek immediate shelter.")
    time.sleep(0.5)
    st.warning("SIMULATION ACTIVE: This is a drill of the regional hazard alert system. No actual emergency is taking place.")
