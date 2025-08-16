import streamlit as st
import numpy as np
from streamlit_folium import st_folium
import folium
from datetime import date, datetime
from sqlalchemy import text

# Establish connection to MySQL using Streamlit connection
conn = st.connection("neon", type="sql")

st.title("BikeSafe CU")
st.sidebar.markdown("Map/Report")

# Set up the interactive Folium map
m = folium.Map(location=[20, 78], zoom_start=4)
m.add_child(folium.LatLngPopup())
map_output = st_folium(m, width=700, height=500)

clicked_coords = map_output.get("last_clicked") if map_output else None

# Incident reporting form
with st.form("f"):
    st.write("To report an incident, click the map, choose the incident type, add a description, and submit!")
    incident = st.selectbox("Incident type:", ['Accidents', 'Thefts', 'Hazards', 'Other Incidents'])
    description = st.text_area("Description:")

    submit = st.form_submit_button('Submit')
    if submit:
        if clicked_coords:
            lat = clicked_coords['lat']
            lng = clicked_coords['lng']
            current_date = date.today()
            current_time = datetime.now().strftime("%H:%M:%S")  # Format time as string for SQL

            # Use `conn.session` for executing INSERT (no result returned)
            with conn.session as session:
                session.execute(
                    text("""
                        INSERT INTO basetable ("Date", "Time", "Latitude", "Longitude", "Type", "Description")
                        VALUES (:date, :time, :lat, :lng, :type, :description)
                    """),
                    params={
                        "date": current_date,
                        "time": current_time,
                        "lat": lat,
                        "lng": lng,
                        "type": incident,
                        "description": description
                    }
                )
                session.commit()

            st.success("Incident Submitted!")
            st.write(f"Latitude: {lat}, Longitude: {lng}")
            st.write(f"Type: {incident}")
            st.write(f"Description: {description}")
        else:
            st.error("Please click on the map to select a location before submitting.")
