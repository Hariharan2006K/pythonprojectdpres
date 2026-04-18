import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Interactive Mapping")
st.caption("Locate emergency shelters and active hazard zones in your vicinity.")

st.markdown("---")

st.markdown("### Local Evacuation Map")
st.write("This map displays simulated real-time shelter locations and active flood zones.")

# Center map on a generic location
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add dummy shelters
folium.Marker(
    [40.7128, -74.0060], popup="City Hall Emergency Shelter", tooltip="Secure Shelter", icon=folium.Icon(color="green", icon="home")
).add_to(m)
folium.Marker(
    [40.7282, -73.9942], popup="NYU Hospital Zone", tooltip="Hospital", icon=folium.Icon(color="red", icon="plus")
).add_to(m)

# Add dummy hazard zone
folium.Circle(
    radius=1200,
    location=[40.7050, -74.0150],
    popup="Active Flood Warning Zone",
    color="crimson",
    fill=True,
).add_to(m)

st_data = st_folium(m, width=800, height=500)

st.info("Interact with the map above to view the details of operational shelters and active hazard zones.")
