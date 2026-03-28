import plotly.express as px
import pandas as pd
import streamlit as st

import utils.data as data
import utils.colors as color

def draw_ticket_volumes(df):

    monthly_counts = data.get_monthly_agg(df)

    # Plotly Chart
    fig = px.line(
        monthly_counts, x="Month", y="ticket_count",
        title="Monthly Ticket Volume", markers=True
    )

    # Shade below line
    fig.update_traces(fill='tozeroy')

    # Ensure last month's label is shown
    x_start = monthly_counts['Month'].min()
    x_end = monthly_counts['Month'].max() + pd.DateOffset(months=1)
    fig.update_layout(
        title_x=0.5,
        title_xanchor='center',
        title_font=dict(size=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis_title='Month',
        yaxis_title='Tickets',
        yaxis=dict(
            range=[0, 130],
            showgrid=True, 
            gridcolor="#30363d", 
            color="#8b949e"
        ),
        xaxis=dict(
            range=[x_start, x_end],
            showgrid=False,
            color="#8b949e",
            tickmode='linear',
            dtick="M1",
            tickformat="%b %Y",
            tickangle=0, 
            nticks=20
        ),
    )
    return fig

def draw_ticket_count(df):
    st.markdown(f"""
        <div style="
            text-align: center;
            background-color: #1e2129; 
            padding: 20px 20px 1px 20px;
            border-radius: 12px; 
            border: 1px solid #30363d;
            display: inline-block;
            min-width: 150px;
            margin-left: 30px;
            margin-bottom: 10px;
        ">
            <p style="
                color: #8b949e; 
                font-size: 0.9rem;
                margin: 0; 
                font-weight: 500;
                letter-spacing: 0.5px;
            ">Total Tickets</p>
            <h2 style="
                color: #ffffff; 
                font-size: 2.2rem;
                margin: -20px 0 0 15px; 
                font-weight: 700;
            ">{len(df)}</h2>
        </div>
    """, unsafe_allow_html=True)

def draw_crt_issue_types(df):
    # Group by month and issue types
    monthly_issues = df.groupby(['Month', 'ClassDownUrg:Type']).size().reset_index(name="issue_count")

    fig = px.bar(
        monthly_issues,
        x="Month",
        y="issue_count",
        color="ClassDownUrg:Type",
        color_discrete_map={
            "General Supplies Issue": color.BLASTER_BLUE,
            "Furniture/Facilities Issue": color.COLORADO_RED,
            "AV / Computer/ Technology issue": color.LIGHT_BLUE
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

    return fig