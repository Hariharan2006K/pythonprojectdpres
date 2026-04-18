import streamlit as st
from fpdf import FPDF
from database import save_score

st.title("Knowledge Assessment")
st.caption("Perform a comprehensive evaluation of your understanding of hazard operational directives.")

# Ensure user is logged in
if not st.session_state.get('logged_in', False):
    st.error("🔒 Operator authentication required. Please log in utilizing the sidebar before engaging the assessment.")
    st.stop()
    
# Function to generate PDF
def generate_pdf(username, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", style="B", size=24)
    pdf.cell(0, 20, "Certificate of Completion", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "This certifies that", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("Helvetica", style="B", size=20)
    pdf.cell(0, 15, username, new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "has successfully passed the DPRES Knowledge Assessment", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 10, f"with a Readiness Score of {score} / 100.", new_x="LMARGIN", new_y="NEXT", align='C')
    return bytes(pdf.output())

# Initialize session state for safety score
if 'safety_score' not in st.session_state:
    st.session_state.safety_score = 0

if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

questions = [
    {
        "q": "1. What is the immediate action you should take during an earthquake?",
        "options": ["Run outside", "Drop, Cover, and Hold On", "Stand in a doorway", "Get in an elevator"],
        "answer": "Drop, Cover, and Hold On"
    },
    {
        "q": "2. What should you do if you are driving when an earthquake starts?",
        "options": ["Speed up to outrun it", "Pull over to a clear location and stay in your car", "Park under a bridge", "Leave your car and run"],
        "answer": "Pull over to a clear location and stay in your car"
    },
    {
        "q": "3. After an earthquake, why should you turn off the main gas valve only if you suspect a leak?",
        "options": ["Because gas is too expensive", "Because only a professional can turn it back on", "Because it makes the house colder", "Because the valve might break"],
        "answer": "Because only a professional can turn it back on"
    },
    {
        "q": "4. What is the safest place to take cover during an earthquake?",
        "options": ["Next to a window", "Under a sturdy piece of furniture", "On the balcony", "Next to a tall bookshelf"],
        "answer": "Under a sturdy piece of furniture"
    },
    {
        "q": "5. What is the golden rule when encountering floodwaters?",
        "options": ["Swim through", "Turn Around, Don't Drown", "Drive slowly", "Measure the depth with a stick"],
        "answer": "Turn Around, Don't Drown"
    },
    {
        "q": "6. Why is it dangerous to walk through floodwaters?",
        "options": ["It can ruin your shoes", "As little as 6 inches of moving water can knock you down", "Water is too cold", "Fishes might bite"],
        "answer": "As little as 6 inches of moving water can knock you down"
    },
    {
        "q": "7. How should you prepare your home for a forecasted flood?",
        "options": ["Open all doors and windows", "Move essential items to upper floors", "Leave electronics plugged in", "Park your car in the basement"],
        "answer": "Move essential items to upper floors"
    },
    {
        "q": "8. What should you do if floodwaters reach your vehicle?",
        "options": ["Stay inside and roll up the windows", "Abandon it and move to higher ground if safe", "Try to push it out", "Reverse out quickly"],
        "answer": "Abandon it and move to higher ground if safe"
    },
    {
        "q": "9. How often should you test your smoke alarms?",
        "options": ["Once a week", "Once a month", "Once a year", "Never"],
        "answer": "Once a month"
    },
    {
        "q": "10. How should you move through a smoke-filled room?",
        "options": ["Run as fast as possible", "Walk upright holding your breath", "Crawl low under the smoke", "Wait for someone to rescue you"],
        "answer": "Crawl low under the smoke"
    },
    {
        "q": "11. If your clothes catch on fire, what should you do?",
        "options": ["Run around to blow out the flames", "Stop, Drop, and Roll", "Take them off immediately", "Find a fan"],
        "answer": "Stop, Drop, and Roll"
    },
    {
        "q": "12. What should you check before opening a closed door during a fire?",
        "options": ["Check if it's locked", "Look under the gap for light", "Feel the door or doorknob with the back of your hand for heat", "Knock first"],
        "answer": "Feel the door or doorknob with the back of your hand for heat"
    },
    {
        "q": "13. What is the calm center of a cyclone/hurricane called?",
        "options": ["The Core", "The Eye", "The Hub", "The Nucleus"],
        "answer": "The Eye"
    },
    {
        "q": "14. During a cyclone, where is the safest place to be inside a house?",
        "options": ["Near a large window to see outside", "In an interior room on the lowest level lacking windows", "On the roof", "In the attic"],
        "answer": "In an interior room on the lowest level lacking windows"
    },
    {
        "q": "15. Why should you board up windows before a cyclone?",
        "options": ["To keep the house warm", "To prevent flying debris from shattering the glass", "To stop rain from coming in", "To keep neighbors out"],
        "answer": "To prevent flying debris from shattering the glass"
    },
    {
        "q": "16. After a cyclone, what should you be highly cautious of when walking outside?",
        "options": ["Fallen trees", "Downed power lines", "Flooded roads", "All of the above"],
        "answer": "All of the above"
    },
    {
        "q": "17. Which is a primary symptom of heat stroke requiring immediate medical attention?",
        "options": ["Heavy sweating", "Cool, pale, clammy skin", "Confusion, passing out, or very high body temperature", "Muscle cramps"],
        "answer": "Confusion, passing out, or very high body temperature"
    },
    {
        "q": "18. What is the most important thing to do during a heatwave?",
        "options": ["Exercise outdoors", "Stay hydrated and drink plenty of water", "Drink sugary or alcoholic beverages", "Keep windows open during the hottest part of the day"],
        "answer": "Stay hydrated and drink plenty of water"
    },
    {
        "q": "19. Which demographic is most vulnerable during a heatwave?",
        "options": ["Teenagers", "Young adults", "The elderly and young children", "Athletes"],
        "answer": "The elderly and young children"
    },
    {
        "q": "20. How can you cool your home without air conditioning?",
        "options": ["Use the oven to bake", "Cover windows with reflectors or closed curtains during the day", "Leave all doors wide open during peak sun hours", "Turn on all incandescent lights"],
        "answer": "Cover windows with reflectors or closed curtains during the day"
    }
]

with st.form("quiz_form"):
    user_answers = []
    for i, q in enumerate(questions):
        st.markdown(f"**{q['q']}**")
        ans = st.radio(f"Options for Q{i+1}", q['options'], key=f"q_{i}", label_visibility="collapsed")
        user_answers.append(ans)
        st.markdown("---")
        
    submitted = st.form_submit_button("Submit Evaluation")
    
    if submitted:
        score = 0
        st.session_state.quiz_submitted = True
        
        st.subheader("Evaluation Results")
        for i, q in enumerate(questions):
            if user_answers[i] == q['answer']:
                score += 5
            else:
                st.error(f"**Q{i+1}: Incorrect** - Selected: '{user_answers[i]}'. Accurate action: '{q['answer']}'.")
                
        st.session_state.safety_score = score
        # Save score to DB
        save_score(st.session_state.user_id, score)

# Display Safety Score
if st.session_state.quiz_submitted:
    st.markdown("---")
    st.markdown(f"### Assessment Score: **{st.session_state.safety_score} / 100**")
    st.progress(st.session_state.safety_score / 100)
    
    if st.session_state.safety_score >= 80:
        st.info("Pass: Operative Readiness Confirmed.")
        st.balloons()
        
        # Generator PDF
        pdf_bytes = generate_pdf(st.session_state.username, st.session_state.safety_score)
        st.download_button(
            label="Download Rescue Certification PDF 🎓",
            data=pdf_bytes,
            file_name="DPRES_Certification.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Fail: Remedial review of the Survival Guides is required.")
