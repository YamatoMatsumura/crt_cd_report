from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import streamlit as st

import utils.data as data 

print("in cd")
st.set_page_config(layout="wide")

cd_df = data.load_cd_data()
cd_df = data.parse_cd_data(cd_df)

st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>Classroom Down</h1>", unsafe_allow_html=True)

date_range = st.date_input("Select Date Range", [cd_df["Created"].min(), cd_df["Created"].max()])

cd_df_filtered = cd_df[
    (cd_df["Created"] >= pd.to_datetime(date_range[0])) &
    (cd_df["Created"] <= pd.to_datetime(date_range[1]))
]

print(cd_df_filtered["Location"].value_counts(dropna=False))
print(cd_df_filtered["Location Room"].value_counts(dropna=False))