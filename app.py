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

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center; color:#d6336c;'>🛡️ Nirbhaya-Path</h1>
    <h4 style='text-align:center;'>AI-Driven Safe Route Navigation (Prototype)</h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🗺️ Route Planner", "📊 Safety Insights", "ℹ️ About Project"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "⚠️ This is a **prototype** developed as a mini project to demonstrate "
    "safe route planning concepts using OpenStreetMap data."
)

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.subheader("🚺 Why Nirbhaya-Path?")
    st.write(
        """
        Many navigation systems focus only on the **shortest route**, not the **safest route**.
        **Nirbhaya-Path** aims to prioritize **user safety**, especially for women,
        by considering environmental and contextual risk factors.
        """
    )

    st.markdown("### 🔐 Key Objectives")
    st.markdown(
        """
        - Improve safety during navigation  
        - Reduce exposure to unsafe or poorly lit areas  
        - Assist users during night or emergency travel  
        """
    )

    st.success("✅ This prototype demonstrates concept, logic, and UI flow.")

# ---------------- ROUTE PLANNER ----------------
elif page == "🗺️ Route Planner":
    st.subheader("🧭 Plan Your Safe Route")

    col1, col2 = st.columns(2)

    with col1:
        start_lat = st.number_input("Start Latitude", value=28.6139, format="%.6f")
        start_lon = st.number_input("Start Longitude", value=77.2090, format="%.6f")

    with col2:
        end_lat = st.number_input("Destination Latitude", value=28.7041, format="%.6f")
        end_lon = st.number_input("Destination Longitude", value=77.1025, format="%.6f")

    st.markdown("📍 *Current location is simulated for prototype purposes.*")

    if st.button("🔍 Generate Safe Route"):
        start = (start_lat, start_lon)
        end = (end_lat, end_lon)

        distance_km = geodesic(start, end).km

        # Simulated safety score logic
        if distance_km < 5:
            safety_score = 85
            safety_label = "🟢 High Safety"
        elif distance_km < 10:
            safety_score = 65
            safety_label = "🟡 Medium Safety"
        else:
            safety_score = 45
            safety_label = "🔴 Low Safety"

        st.markdown(f"### 🛡️ Safety Score: **{safety_score}/100** ({safety_label})")
        st.caption("Score is calculated using distance-based risk approximation (prototype logic).")

        # Create map
        route_map = folium.Map(location=start, zoom_start=12)

        folium.Marker(
            start,
            popup="Start Location",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(route_map)

        folium.Marker(
            end,
            popup="Destination",
            icon=folium.Icon(color="red", icon="stop")
        ).add_to(route_map)

        folium.PolyLine(
            locations=[start, end],
            color="blue",
            weight=5,
            tooltip="Simulated Safe Route"
        ).add_to(route_map)

        st_folium(route_map, width=900, height=500)

# ---------------- SAFETY INSIGHTS ----------------
elif page == "📊 Safety Insights":
    st.subheader("📊 Safety Parameters Considered")

    st.markdown(
        """
        The following parameters are considered in a **full-scale implementation**:

        - Street lighting density  
        - Nearby police stations  
        - Crowd density  
        - Historical incident data  
        - Time of travel (day/night)  
        """
    )

    st.warning(
        "⚠️ In this prototype, safety is simulated. "
        "Real-world deployment uses graph-based routing."
    )

    st.markdown("### 🧠 Technical Stack (Planned)")
    st.code(
        """
        OSMnx     → Fetch real street network from OpenStreetMap
        NetworkX → Graph-based pathfinding (Dijkstra / A*)
        AI Model → Safety score prediction
        Streamlit → Frontend visualization
        """
    )

# ---------------- ABOUT ----------------
elif page == "ℹ️ About Project":
    st.subheader("ℹ️ Project Information")

    st.markdown(
        """
        **Project Name:** Nirbhaya-Path  
        **Domain:** Smart Cities / Women Safety  
        **Type:** Mini Project (Prototype)  

        ### 👨‍💻 Why Prototype?
        This project focuses on:
        - Concept validation  
        - UI/UX flow  
        - Algorithmic design  

        Full deployment requires:
        - Government & public safety data
        - Paid map APIs
        - Mobile GPS permissions
        """
    )

    st.success("🎓 Designed for academic demonstration and evaluation.")
