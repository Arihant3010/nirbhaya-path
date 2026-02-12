import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Nirbhaya-Path",
    page_icon="🛡️",
    layout="centered"   # mobile feel
)

# ---------------- THEME ----------------
st.markdown("""
<style>
.main { background-color: #0b0b0b; }
h1, h2, h3, h4, h5, p, label { color: #f5c518; }
div[data-testid="stMetric"] {
    background-color: #111;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
for key in ["logged", "user", "start", "end"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ---------------- LOGIN / REGISTER ----------------
def auth_page():
    st.markdown("<h2 style='text-align:center;'>🔐 Nirbhaya-Path</h2>", unsafe_allow_html=True)
    st.caption("Register or Login to continue")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Mobile Number")
    city = st.text_input("City")

    if st.button("Register / Login"):
        if name and email and phone and city:
            st.session_state.logged = True
            st.session_state.user = name
            st.success("Login Successful")
        else:
            st.error("Please fill all details")

if not st.session_state.logged:
    auth_page()
    st.stop()

# ---------------- SIDEBAR (HAMBURGER MENU) ----------------
menu = st.sidebar.radio(
    "☰ Menu",
    [
        "🏠 Dashboard",
        "🧭 Find Safe Route",
        "🚨 SOS",
        "📝 Feedback",
        "📢 Complaints",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption(f"👤 {st.session_state.user}")

# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":
    st.subheader("🛡️ Safety Dashboard")

    st.metric("User Status", "Protected")
    st.metric("Last Safety Score", "—")
    st.metric("Emergency Ready", "YES")

    st.info("Use **Find Safe Route** to start navigation.")

# ---------------- SAFE ROUTE ----------------
elif menu == "🧭 Find Safe Route":
    st.subheader("🧭 Enter Coordinates")

    start_lat = st.number_input("Start Latitude", value=19.2506, format="%.6f")
    start_lon = st.number_input("Start Longitude", value=72.8745, format="%.6f")

    end_lat = st.number_input("Destination Latitude", value=19.1860, format="%.6f")
    end_lon = st.number_input("Destination Longitude", value=72.9759, format="%.6f")

    if st.button("📍 Set Locations"):
        st.session_state.start = (start_lat, start_lon)
        st.session_state.end = (end_lat, end_lon)
        st.success("Locations set successfully")

    if st.session_state.start and st.session_state.end:
        # Simulated routes
        safe_route = [
            st.session_state.start,
            ((start_lat+end_lat)/2 + 0.01, (start_lon+end_lon)/2),
            st.session_state.end
        ]
        unsafe_route = [
            st.session_state.start,
            ((start_lat+end_lat)/2 - 0.01, (start_lon+end_lon)/2 - 0.01),
            st.session_state.end
        ]

        distance = round(geodesic(st.session_state.start, st.session_state.end).km, 2)
        time = round(distance / 30 * 60, 1)  # minutes
        safety_score = max(100 - int(distance * 3), 45)

        if st.button("🛡️ Find Safest Route"):
            st.subheader("🗺️ Route Comparison")

            m = folium.Map(location=st.session_state.start, zoom_start=12)

            folium.Marker(st.session_state.start, popup="Start", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker(st.session_state.end, popup="Destination", icon=folium.Icon(color="red")).add_to(m)

            # Safe route
            folium.PolyLine(safe_route, color="green", weight=6, tooltip="Safest Route").add_to(m)
            folium.PolyLine(unsafe_route, color="red", weight=4, tooltip="Less Safe Route").add_to(m)

            # Safety markers
            folium.Marker(safe_route[1], popup="24×7 Shop", icon=folium.Icon(color="blue")).add_to(m)
            folium.Marker((safe_route[1][0]+0.005, safe_route[1][1]), popup="Crowded Area", icon=folium.Icon(color="purple")).add_to(m)
            folium.Marker((safe_route[1][0]-0.005, safe_route[1][1]), popup="Police Station", icon=folium.Icon(color="cadetblue")).add_to(m)

            st_folium(m, height=450, width=350)

            st.metric("Safety Score", f"{safety_score}/100")
            st.metric("Distance", f"{distance} km")
            st.metric("Approx Time", f"{time} mins")

# ---------------- SOS ----------------
elif menu == "🚨 SOS":
    st.subheader("🚨 Emergency Assistance")

    st.error("Press only in real emergency (Prototype)")
    if st.button("ACTIVATE SOS"):
        st.error("🚨 SOS ACTIVATED")
        st.write("• Emergency contacts notified")
        st.write("• Nearest police alerted")
        st.write("• Location shared")

# ---------------- FEEDBACK ----------------
elif menu == "📝 Feedback":
    st.subheader("📝 User Feedback")
    feedback = st.text_area("Your experience")
    if st.button("Submit"):
        st.success("Thank you for helping us improve")

# ---------------- COMPLAINTS ----------------
elif menu == "📢 Complaints":
    st.subheader("📢 Safety Complaint")
    st.text_input("Location")
    st.text_area("Describe incident")
    if st.button("Register Complaint"):
        st.success("Complaint registered (Prototype)")

# ---------------- ABOUT ----------------
elif menu == "ℹ️ About":
    st.subheader("ℹ️ About Nirbhaya-Path")
    st.markdown("""
    **Nirbhaya-Path** is a women-safety focused navigation prototype.

    ### Features
    - Safe route prioritization
    - Emergency SOS
    - Community safety markers
    - Mobile-first design

    ### Technology
    - OpenStreetMap
    - Streamlit
    - Planned: OSMnx + NetworkX
    """)

st.caption("⚠️ Prototype for academic evaluation only")
