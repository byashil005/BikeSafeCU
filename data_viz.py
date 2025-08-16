import streamlit as st
import pandas as pd
import pydeck

st.title("Previous Incidents")
st.sidebar.markdown("Map/Report")

chart_data = pd.read_csv("master.csv")

chart_data["Latitude"] = chart_data["Latitude"].astype(float)
chart_data["Longitude"] = chart_data["Longitude"].astype(float)

point_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=chart_data,
    id="chart_data",
    get_position=["Longitude", "Latitude"],
    get_color="[200, 30, 0, 50]",
    pickable=True,
    auto_highlight=True,
    get_radius = 100,
)

view_state = pydeck.ViewState(
    latitude=40.110320,
    longitude=-88.228865,
    controller=True, 
    zoom=2.4, 
    pitch=0
)

chart = pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "{Date}\nType: {Category}\nDescription: {Description}"},
)

event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

event.selection
