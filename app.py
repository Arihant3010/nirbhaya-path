import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Nirbhaya-Path",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3, h4, h5 {
    color: #f1f1f1;
}
.metric-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style="text-align:center;">🛡️ Nirbhaya-Path</h1>
<h4 style="text-align:center; color:#9aa0a6;">
AI-Driven Safe Route Navigation (Prototype)
</h4>
<p style="text-align:center; color:#6c757d;">
SDG-5 • SDG-11 • Women Safety • Smart Cities
</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## ⚙️ Route Settings")

start_lat = st.sidebar.number_input("📍 Start Latitude", value=28.6139, format="%.6f")
start_lon = st.sidebar.number_input("📍 Start Longitude", value=77.2090, format="%.6f")

end_lat = st.sidebar.number_input("🏁 Destination Latitude", value=28.7041, format="%.6f")
end_lon = st.sidebar.number_input("🏁 Destination Longitude", value=77.1025, format="%.6f")

time_mode = st.sidebar.selectbox("🕒 Time of Travel", ["Day", "Night"])
user_type = st.sidebar.selectbox("👤 User Type", ["Student", "Working Professional", "General"])

generate = st.sidebar.button("🚦 Generate Safest Route")

# ---------------- MAIN TABS ----------------
tab1, tab2, tab3 = st.tabs(["🗺️ Route Map", "📊 Safety Analysis", "ℹ️ About"])

# ---------------- ROUTE LOGIC ----------------
start = (start_lat, start_lon)
end = (end_lat, end_lon)
distance_km = round(geodesic(start, end).km, 2)

# Simulated AI safety logic
risk = 0
risk += 20 if time_mode == "Night" else 5
risk += 10 if distance_km > 10 else 5
risk += 5 if user_type == "Student" else 10

safety_score = max(100 - risk, 30)

# ---------------- TAB 1: MAP ----------------
with tab1:
    st.subheader("🗺️ Safe Route Visualization")

    m = folium.Map(
        location=start,
        zoom_start=12,
        tiles="CartoDB dark_matter"
    )

    folium.Marker(
        start,
        popup="Start Location",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)

    folium.Marker(
        end,
        popup="Destination",
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(m)

    folium.PolyLine(
        locations=[start, end],
        tooltip="Safest Route (Prototype)",
        color="#00ff9c",
        weight=6
    ).add_to(m)

    st_folium(m, width=1200, height=520)

# ---------------- TAB 2: SAFETY DASHBOARD ----------------
with tab2:
    st.subheader("📊 Safety Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"<div class='metric-card'><h2>{safety_score}/100</h2><p>Safety Score</p></div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"<div class='metric-card'><h2>{distance_km} km</h2><p>Route Distance</p></div>",
            unsafe_allow_html=True
        )

    with col3:
        level = "High" if safety_score > 70 else "Medium" if safety_score > 50 else "Low"
        st.markdown(
            f"<div class='metric-card'><h2>{level}</h2><p>Risk Level</p></div>",
            unsafe_allow_html=True
        )

    st.markdown("### 🤖 AI Safety Explanation")

    if time_mode == "Night":
        st.info(
            "This route was selected to minimize exposure to isolated and poorly lit areas. "
            "Night-time risk penalties were applied, prioritizing main roads and public zones."
        )
    else:
        st.info(
            "Day-time routing focuses on balanced safety and accessibility using low-risk road segments."
        )

# ---------------- TAB 3: ABOUT ----------------
with tab3:
    st.subheader("ℹ️ About Nirbhaya-Path")

    st.markdown("""
**Nirbhaya-Path** is an AI-assisted safe route navigation prototype designed
to prioritize user safety over speed.

### 🔧 Planned Full Implementation
- **OSMnx** → Extract real street networks from OpenStreetMap  
- **NetworkX** → Graph-based routing (Dijkstra / A*)  
- **AI Models** → Dynamic risk prediction  
- **Mobile GPS** → Real-time location  

⚠️ Current version uses simulated logic for academic demonstration.
""")

st.markdown("---")
st.caption("Mini Project • Software Engineering • AI-Assisted Prototype • College Panel Demo")
