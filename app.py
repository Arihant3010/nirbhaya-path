import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Nirbhaya-Path", page_icon="🛡️", layout="wide")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "start" not in st.session_state:
    st.session_state.start = None
if "end" not in st.session_state:
    st.session_state.end = None

# ---------------- AUTH ----------------
def login_ui():
    st.subheader("🔐 Login / Register")
    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Login / Register"):
        if name and email:
            st.session_state.logged_in = True
            st.session_state.user = name
            st.success("Logged in successfully")
        else:
            st.error("Please enter details")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style="text-align:center;">🛡️ Nirbhaya-Path</h1>
<p style="text-align:center;color:gray;">
AI-Driven Safe Route Navigation • SDG-5 • SDG-11
</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- LOGIN CHECK ----------------
if not st.session_state.logged_in:
    login_ui()
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.markdown(f"### 👤 Welcome, {st.session_state.user}")
time_mode = st.sidebar.selectbox("🕒 Time of Travel", ["Day", "Night"])

if st.sidebar.button("🚨 SOS"):
    st.sidebar.error("🚨 SOS ACTIVATED")
    st.sidebar.write("Emergency alert sent to nearby authorities (prototype).")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 Feedback")
feedback = st.sidebar.text_area("Your feedback")
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your feedback!")

# ---------------- MAIN ----------------
tabs = st.tabs(["🗺️ Map & Route", "📊 Safety Layers", "📸 Camera", "ℹ️ About"])

# ---------------- MAP TAB ----------------
with tabs[0]:
    st.subheader("🗺️ Select Start & Destination")

    m = folium.Map(location=[28.6139, 77.2090], zoom_start=12, tiles="CartoDB positron")

    # Demo safety layers
    folium.Marker([28.616, 77.210], popup="24x7 Shop", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker([28.620, 77.215], popup="Crowded Area", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker([28.608, 77.200], popup="Unsafe Zone", icon=folium.Icon(color="red")).add_to(m)

    map_data = st_folium(m, height=500, width=1200)

    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]

        if st.session_state.start is None:
            st.session_state.start = (lat, lon)
            st.success("Start point selected")
        else:
            st.session_state.end = (lat, lon)
            st.success("Destination selected")

    if st.session_state.start and st.session_state.end:
        distance = round(geodesic(st.session_state.start, st.session_state.end).km, 2)

        risk = 20 if time_mode == "Night" else 8
        safety_score = max(100 - risk - int(distance), 40)

        if st.button("🛡️ Find Safest Route"):
            route_map = folium.Map(location=st.session_state.start, zoom_start=13)

            folium.Marker(st.session_state.start, popup="Start", icon=folium.Icon(color="green")).add_to(route_map)
            folium.Marker(st.session_state.end, popup="End", icon=folium.Icon(color="red")).add_to(route_map)

            folium.PolyLine(
                [st.session_state.start, st.session_state.end],
                color="blue",
                weight=6,
                tooltip="Safest Route (Prototype)"
            ).add_to(route_map)

            st_folium(route_map, height=500, width=1200)

            st.info(f"🛡️ Safety Score: {safety_score}/100")

# ---------------- SAFETY LAYERS ----------------
with tabs[1]:
    st.subheader("📊 Safety Indicators Used")
    st.markdown("""
    - ✔️ 24×7 Shops & Medical Stores  
    - ✔️ Crowded / Active Areas  
    - ✔️ Time of Travel  
    - ✔️ Distance & Isolation  
    """)
    st.warning("Live data integration via OSMnx & NetworkX is planned.")

# ---------------- CAMERA ----------------
with tabs[2]:
    st.subheader("📸 Capture / Upload Evidence")
    image = st.file_uploader("Upload image (Camera Prototype)", type=["jpg", "png"])
    if image:
        st.image(image, caption="Uploaded Image")

# ---------------- ABOUT ----------------
with tabs[3]:
    st.markdown("""
    **Nirbhaya-Path** is a prototype designed for academic evaluation.

    ### 🔧 Future Scope
    - Real GPS location
    - OSMnx street graph extraction
    - NetworkX safest-path algorithms
    - Real SOS & authority integration
    """)

st.caption("Mini Project • AI-Assisted Prototype • College Panel Demo")
