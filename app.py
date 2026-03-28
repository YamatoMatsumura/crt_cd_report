import streamlit as st

overview = st.Page("pages/overview.py", title="Ticket Overview", default=True)
# cd = st.Page("pages/classroom_down.py", title="Classroom Down Dashboard")
crt = st.Page("pages/crt.py", title="CRT Dashboard")

# pg = st.navigation([overview, crt, cd])
pg = st.navigation([overview, crt])
pg.run()