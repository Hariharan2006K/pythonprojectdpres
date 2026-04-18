import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_dashboard_stats

st.title("Readiness Metrics")
st.caption("Review institutional engagement data and incident statistics powered by real-time database inputs.")

total_users, avg_score, total_sims, recent_scores = get_dashboard_stats()

# --- Key Metrics ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Registered Personnel", value=total_users, delta="Live Data")
with col2:
    st.metric(label="Mean Assessment Score", value=f"{avg_score:.1f}/100" if avg_score else "N/A", delta="Live Data")
with col3:
    st.metric(label="Simulations Conducted", value=total_sims, delta="Live Data")
with col4:
    st.metric(label="Active Regional Nodes", value=12, delta="Steady")

st.markdown("---")

# Row 1: Interactive Charts
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.markdown("### Recent Evaluation Activity")
    # Real data from SQLite DB
    if len(recent_scores) > 0:
        df_scores = pd.DataFrame(recent_scores, columns=["Operator", "Score", "Timestamp"])
        # Format Timestamp
        df_scores['Timestamp'] = pd.to_datetime(df_scores['Timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(df_scores, use_container_width=True, hide_index=True)
    else:
        st.info("No recorded assessment attempts yet. Log in and conduct an evaluation.")

with r1c2:
    st.markdown("### Regional Incident Distribution")
    # Pie Chart Data (Mocking historical data context)
    pie_data = {
        "Hazard Type": ["Earthquakes", "Floods", "Fires", "Cyclones", "Heatwaves"],
        "Reported Instances": [15, 45, 20, 10, 30]
    }
    df_pie = pd.DataFrame(pie_data)
    
    fig_pie = px.pie(
        df_pie, 
        names="Hazard Type", 
        values="Reported Instances", 
        title="Historical Callouts by Hazard",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Row 2: Line Chart
st.markdown("### Simulated Drill Attendance Trajectory")
# Line Chart Data (Mock representing theoretical engagement)
line_data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "Attendance (%)": [35, 38, 42, 40, 55, 60, 65, 70, 75, 78, 80, 82]
}
df_line = pd.DataFrame(line_data)

fig_line = px.line(
    df_line, 
    x="Month", 
    y="Attendance (%)", 
    markers=True,
    title="Participation Rate Over Cycle",
    labels={"Attendance (%)": "Participation Rate (%)"}
)
fig_line.update_traces(line_color="#1F77B4", line_width=3, marker_size=8)
fig_line.update_layout(margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_line, use_container_width=True)
