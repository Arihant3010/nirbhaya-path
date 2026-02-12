import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Nirbhaya-Path",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- THEME ----------------
st.markdown("""
<style>
.main { background-color: #0b0b0b; }
h1, h2, h3, p, label { color: #f5c518; }
.card {
    background: #111;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "logged" not in st.session_state:
    st.session_state.logged = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "show_route" not in st.session_state:
    st.session_state.show_route = False

# =================================================
# 🔐 LOGIN / REGISTER (ALWAYS FIRST)
# =================================================
if not st.session_state.logged:
    st.markdown("<h2 style='text-align:center;'>🛡️ Nirbhaya-Path</h2>", unsafe_allow_html=True)
    st.caption("Safe Route Navigation for Women")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Mobile Number")
    city = st.text_input("City")

    if st.button("Login / Register"):
        if name and email and phone and city:
            st.session_state.logged = True
            st.session_state.user = name
            st.experimental_rerun()
        else:
            st.error("Please fill all details")

    st.stop()   # ⛔ CRITICAL: stops app here

# =================================================
# ☰ SIDEBAR MENU
# =================================================
menu = st.sidebar.radio(
    "☰ Menu",
    ["🧭 Safe Route", "🚨 SOS", "📝 Feedback", "ℹ️ About"]
)
st.sidebar.caption(f"👤 {st.session_state.user}")

# =================================================
# 🧭 SAFE ROUTE PAGE
# =================================================
if menu == "🧭 Safe Route":
    st.markdown(f"<h3>Hello, {st.session_state.user}</h3>", unsafe_allow_html=True)
    st.caption("Choose safety over speed.")

    st.markdown("<div class='card'>📍 Enter Coordinates</div>", unsafe_allow_html=True)

    start_lat = st.number_input("Start Latitude", value=19.2506, format="%.6f")
    start_lon = st.number_input("Start Longitude", value=72.8745, format="%.6f")

    end_lat = st.number_input("Destination Latitude", value=19.1860, format="%.6f")
    end_lon = st.number_input("Destination Longitude", value=72.9759, format="%.6f")

    start = (start_lat, start_lon)
    end = (end_lat, end_lon)

    if st.button("🛡️ Find Safest Route"):
        st.session_state.show_route = True

    # ---------------- MAP (ALWAYS RENDERED) ----------------
    m = folium.Map(
        location=start,
        zoom_start=12,
        tiles="CartoDB dark_matter"
    )

    folium.Marker(start, popup="Start", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(end, popup="Destination", icon=folium.Icon(color="red")).add_to(m)

    if st.session_state.show_route:
        safe_route = [
            start,
            ((start_lat + end_lat) / 2 + 0.01, (start_lon + end_lon) / 2),
            end
        ]
        unsafe_route = [
            start,
            ((start_lat + end_lat) / 2 - 0.01, (start_lon + end_lon) / 2 - 0.01),
            end
        ]

        folium.PolyLine(safe_route, color="green", weight=6, tooltip="Safest Route").add_to(m)
        folium.PolyLine(unsafe_route, color="red", weight=4, tooltip="Less Safe Route").add_to(m)

        # Safety markers
        folium.Marker(safe_route[1], popup="24×7 Shop", icon=folium.Icon(color="blue")).add_to(m)
        folium.Marker((safe_route[1][0] + 0.005, safe_route[1][1]),
                      popup="Crowded Area", icon=folium.Icon(color="purple")).add_to(m)
        folium.Marker((safe_route[1][0] - 0.005, safe_route[1][1]),
                      popup="Police Station", icon=folium.Icon(color="cadetblue")).add_to(m)

    st_folium(m, height=420, width=350)

    # ---------------- DETAILS ----------------
    if st.session_state.show_route:
        distance = round(geodesic(start, end).km, 2)
        time = round(distance / 30 * 60, 1)
        safety_score = max(85 - int(distance * 2), 45)

        st.markdown("<div class='card'>📊 Route Details</div>", unsafe_allow_html=True)
        st.metric("Safety Score", f"{safety_score}/100")
        st.metric("Distance", f"{distance} km")
        st.metric("Approx Time", f"{time} mins")

# =================================================
# 🚨 SOS PAGE
# =================================================
elif menu == "🚨 SOS":
    st.subheader("🚨 Emergency SOS")
    st.error("Prototype – Use only in emergency")

    if st.button("ACTIVATE SOS"):
        st.error("🚨 SOS ACTIVATED")
        st.write("• Location shared")
        st.write("• Police notified")
        st.write("• Emergency contacts alerted")

# =================================================
# 📝 FEEDBACK
# =================================================
elif menu == "📝 Feedback":
    st.subheader("📝 Feedback")
    st.text_area("Your feedback")
    if st.button("Submit"):
        st.success("Thank you for your feedback")

# =================================================
# ℹ️ ABOUT
# =================================================
elif menu == "ℹ️ About":
    st.subheader("ℹ️ About Nirbhaya-Path")
    st.markdown("""
    Nirbhaya-Path is a women-safety focused navigation prototype.

    **Key Focus**
    - Safe route prioritization
    - Emergency assistance
    - Mobile-first UX

    **Future Scope**
    - Real GPS
    - OSMnx street graphs
    - NetworkX routing
    - Native mobile app
    """)

st.caption("Prototype for academic evaluation only")
