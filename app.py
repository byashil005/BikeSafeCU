import streamlit as st

st.sidebar.title("BikeSafe CU")

page1 = st.Page("report.py", title = "Map/Report")
page2 = st.Page("data_viz.py", title = "Data Visualization")
page3 = st.Page("about.py", title = "About")

pg = st.navigation([page1, page2, page3])

pg.run()
