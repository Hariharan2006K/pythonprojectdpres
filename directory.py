import streamlit as st
import pandas as pd

st.title("SOS Directory")
st.caption("Access critical emergency hotlines natively.")

st.markdown("---")

region = st.selectbox("Select Your Region", ["North America", "Europe", "Asia", "Oceania"])

if region == "North America":
    data = {"Service": ["General Emergency", "Poison Control", "FEMA Hotline", "Red Cross"], "Number": ["911", "1-800-222-1222", "1-800-621-3362", "1-800-RED-CROSS"]}
elif region == "Europe":
    data = {"Service": ["General Emergency", "Medical Advice", "Fire Brigade", "Police"], "Number": ["112", "111 (UK)", "112 / 18 (FR)", "112 / 17 (FR)"]}
elif region == "Asia":
    data = {"Service": ["General Emergency (India)", "General Emergency (Japan)", "Disaster Help (India)", "Ambulance (China)"], "Number": ["112", "119", "1078", "120"]}
else:
    data = {"Service": ["General Emergency (Aus)", "SES Flood/Storm (Aus)", "General Emergency (NZ)"], "Number": ["000", "132 500", "111"]}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True, hide_index=True)

st.info(f"The numbers displayed above are active emergency lines for {region}. Note: Always prioritize life safety before property.")
