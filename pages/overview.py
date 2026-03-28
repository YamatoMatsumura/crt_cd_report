import streamlit as st

import utils.data as data
import utils.visuals as visuals

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>Ticket Overview</h1>", unsafe_allow_html=True)

# Creating a structured layout
_, left, right, _ = st.columns([0.5, 4, 4, 0.5])

with left:
    cd_df = data.load_cd_data()
    cd_df = data.parse_cd_data(cd_df)

    st.markdown("<h2 style='text-align: center; color: var(--text-color); font-weight: 200; margin-bottom: 0px;'>Classroom Down</h2>", unsafe_allow_html=True)
    
    visuals.draw_ticket_count(cd_df)

    st.plotly_chart(visuals.draw_ticket_volumes(cd_df), width='stretch')

with right:
    crt_df = data.load_crt_data()
    crt_df = data.parse_crt_data(crt_df)

    st.markdown("<h2 style='text-align: center; color: var(--text-color); font-weight: 200; margin-bottom: 0px;'>Classroom Response Team</h2>", unsafe_allow_html=True)

    visuals.draw_ticket_count(crt_df)

    st.plotly_chart(visuals.draw_ticket_volumes(crt_df), width='stretch')