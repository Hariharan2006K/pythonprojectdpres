import streamlit as st

st.title("Go-Bag Builder")
st.caption("Pack your digital survival kit and check your preparedness readiness score.")

st.markdown("---")

items = [
    "Water (1 gallon per person per day for 3 days)",
    "Non-perishable food (3-day supply)",
    "Battery-powered or hand-crank radio",
    "Flashlight with extra batteries",
    "First aid kit",
    "Whistle (to signal for help)",
    "Dust mask (to filter contaminated air)",
    "Moist towelettes and garbage bags (for personal sanitation)",
    "Wrench or pliers (to turn off utilities)",
    "Manual can opener",
    "Local maps",
    "Cell phone with chargers and backup battery"
]

st.write("Check off the items you currently possess in your emergency kit:")

checked_items = []
for i, item in enumerate(items):
    checked = st.checkbox(item, key=f"gobag_{i}")
    if checked:
        checked_items.append(item)

st.markdown("---")
progress = len(checked_items) / len(items)

st.progress(progress)
st.markdown(f"**Preparedness Readiness:** {len(checked_items)} / {len(items)} items ({int(progress*100)}%)")

if progress == 1.0:
    st.success("Your Go-Bag is fully packed and ready for deployment!")
elif progress > 0.5:
    st.warning("Good progress, but you are still missing some critical operational items.")
else:
    st.error("Your Go-Bag is insufficient for a 72-hour survival scenario. Please procure these items immediately.")
