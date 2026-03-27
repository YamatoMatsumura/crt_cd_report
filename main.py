import streamlit as st

overview = st.Page("app.py", title="Ticket Overview", default=True)
crt = st.Page("pages/crt_dashboard.py", title="CRT Dashboard")
cd = st.Page("pages/classroom_down_dashboard.py", title="Classroom Down Dashboard")

pg = st.navigation([overview, crt, cd])
pg.run()