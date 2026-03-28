import pandas as pd
from pathlib import Path
from datetime import datetime
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px


import utils.data as data


st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>CRT</h1>", unsafe_allow_html=True)

crt_df = data.load_crt_data()
crt_df = data.parse_crt_data(crt_df)

BLASTER_BLUE = "#09396C"
LIGHT_BLUE = "#879EC3"
DARK_BLUE = "#21314d"
COLORADO_RED = "#CC4628"

# monthly volumms
crt_df['Month'] = crt_df['Created'].dt.to_period('M').apply(lambda r: r.start_time)

# crt tickets by month and issues
monthly_issues = crt_df.groupby(['Month', 'ClassDownUrg:Type']).size().reset_index(name="issue_count")

fig = px.bar(
    monthly_issues,
    x="Month",
    y="issue_count",
    color="ClassDownUrg:Type",
    color_discrete_map={
        "General Supplies Issue": BLASTER_BLUE,
        "Furniture/Facilities Issue": COLORADO_RED,
        "AV / Computer/ Technology issue": LIGHT_BLUE
    },
    barmode="stack",
    labels={"ClassDownUrg:Type": "Issue Type"},
    category_orders={
        "ClassDownUrg:Type": [
            "General Supplies Issue",
            "Furniture/Facilities Issue",
            "AV / Computer/ Technology issue"
        ]
    }
)

fig.update_layout(
    title_text="Issue Types Over Time",
    title_x=0.5,
    title_xanchor='center',
    title_font=dict(size=20),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=50, b=0),
    xaxis_title='Month',
    yaxis_title='Tickets',
    legend_traceorder='reversed'
)

st.plotly_chart(fig, width='stretch')
