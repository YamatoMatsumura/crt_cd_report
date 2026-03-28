import streamlit as st

import utils.data as data
import utils.visuals as visuals


st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>CRT</h1>", unsafe_allow_html=True)

crt_df = data.load_crt_data()
crt_df = data.parse_crt_data(crt_df)

st.plotly_chart(visuals.draw_crt_issue_types(crt_df), width='stretch')
