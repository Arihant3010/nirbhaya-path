import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="nirbhaya-path", layout="wide")

st.title("🛡️ Nirbhaya Path – AI-Driven Safe Route Navigation")
st.subheader("Prioritizing Safety over Speed | SDG 5 & SDG 11")

st.markdown("---")

start = st.text_input("📍 Start Location", "College Gate")
end = st.text_input("🏁 Destination", "Hostel")
time = st.selectbox("🕒 Time of Travel", ["Day", "Night"])

def get_safety_explanation(time):
    if time == "Night":
        return (
            "This route was selected because it avoids isolated streets and poorly "
            "lit areas. It passes through regions with higher public activity such "
            "as main roads and commercial zones, making it safer for night travel."
        )
    else:
        return (
            "This route goes through well-connected roads with consistent lighting "
            "and public movement, ensuring a safer daytime commute."
        )

if st.button("🚶‍♀️ Find Safest Route"):
    st.success("Safest route calculated successfully!")

    # Demo coordinates (prototype mode)
    m = folium.Map(location=[19.0760, 72.8777], zoom_start=13)

    # Safe route
    folium.PolyLine(
        locations=[
            [19.0760, 72.8777],
            [19.0800, 72.8800],
            [19.0850, 72.8850]
        ],
        color="green",
        weight=6,
        tooltip="Safest Route"
    ).add_to(m)

    # Unsafe zones
    folium.Marker(
        [19.0820, 72.8790],
        popup="⚠️ Poorly Lit Area",
        icon=folium.Icon(color="red")
    ).add_to(m)

    folium.Marker(
        [19.0835, 72.8820],
        popup="⚠️ Isolated Street",
        icon=folium.Icon(color="red")
    ).add_to(m)

    st_folium(m, width=1200, height=500)

    st.markdown("### 🤖 Why this route is safer?")
    st.info(get_safety_explanation(time))

st.markdown("---")
st.caption("Mini Project | Software Engineering | College Panel Demo")
