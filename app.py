import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Nirbhaya-Path", page_icon="🛡️", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style="text-align:center;">🛡️ Nirbhaya-Path</h1>
<h4 style="text-align:center; color:gray;">
Safe Route Navigation Prototype (APS Shah → Thane Station)
</h4>
<hr>
""", unsafe_allow_html=True)

# ---------------- FIXED LOCATIONS ----------------
start = (19.2506, 72.8745)   # APS Shah
end = (19.1860, 72.9759)     # Thane Station

# ---------------- ROUTES (SIMULATED) ----------------
safe_route = [
    start,
    (19.2350, 72.9000),
    (19.2200, 72.9300),
    (19.2050, 72.9550),
    end
]

unsafe_route = [
    start,
    (19.2400, 72.8900),
    (19.2250, 72.9150),
    (19.2100, 72.9400),
    end
]

safe_distance = round(geodesic(start, end).km + 2.5, 2)
unsafe_distance = round(geodesic(start, end).km, 2)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🧭 Route Options")

route_choice = st.sidebar.radio(
    "Choose Route Type",
    ["Safest Route (Recommended)", "Less Safe Route"]
)

st.sidebar.markdown("### 🚨 Emergency")
if st.sidebar.button("SOS"):
    st.sidebar.error("🚨 SOS Triggered (Prototype)")
    st.sidebar.write("Alert sent to nearby authorities.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 Feedback")
st.sidebar.text_area("Your feedback")

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([2, 1])

# ---------------- MAP ----------------
with col1:
    st.subheader("🗺️ Route Visualization")

    m = folium.Map(location=start, zoom_start=12, tiles="CartoDB positron")

    folium.Marker(start, popup="APS Shah Institute", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(end, popup="Thane Railway Station", icon=folium.Icon(color="red")).add_to(m)

    # Safety markers
    folium.Marker((19.2350, 72.9000), popup="24×7 Medical Store", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker((19.2200, 72.9300), popup="Crowded Market Area", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker((19.2050, 72.9550), popup="Police Station Nearby", icon=folium.Icon(color="blue")).add_to(m)

    if route_choice == "Safest Route (Recommended)":
        folium.PolyLine(
            safe_route,
            color="green",
            weight=6,
            tooltip="Safest Route"
        ).add_to(m)
    else:
        folium.PolyLine(
            unsafe_route,
            color="red",
            weight=6,
            tooltip="Less Safe Route"
        ).add_to(m)

    st_folium(m, height=520, width=900)

# ---------------- INFO PANEL ----------------
with col2:
    st.subheader("📊 Route Details")

    if route_choice == "Safest Route (Recommended)":
        st.success("🟢 SAFEST ROUTE SELECTED")
        st.metric("Safety Score", "85 / 100")
        st.metric("Distance", f"{safe_distance} km")
        st.markdown("""
        ✔️ Well-lit roads  
        ✔️ 24×7 shops nearby  
        ✔️ Crowded areas  
        ✔️ Police access  
        """)
    else:
        st.warning("🔴 LESS SAFE ROUTE")
        st.metric("Safety Score", "48 / 100")
        st.metric("Distance", f"{unsafe_distance} km")
        st.markdown("""
        ⚠️ Isolated roads  
        ⚠️ Fewer shops  
        ⚠️ Low activity areas  
        """)

    st.markdown("---")
    st.info("""
    Safety scores are calculated using:
    - Distance
    - Area activity
    - Infrastructure presence
    - Time-based risk (prototype logic)
    """)

# ---------------- FOOTER ----------------
st.caption("""
Prototype built using OpenStreetMap.
Future implementation uses OSMnx + NetworkX for real graph-based routing.
""")
