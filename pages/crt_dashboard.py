import pandas as pd
from pathlib import Path
from datetime import datetime
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px


def main():

    st.title("CRT Dashboard")


    TODAY = str(datetime.today().date())

    excel_folder_path = Path("data")

    classroom_down_path = None
    crt_path = None
    for item in excel_folder_path.iterdir():
        if item.is_file():
            if "CRT Tickets" in item.name:
                crt_path = f"{excel_folder_path}/{item.name}"

    crt_df = pd.read_excel(crt_path)


    # rename classroom down types for clarity
    conditions = [
        crt_df['ClassDownUrg:Type'].str.contains("General Supplies", na=False),
        crt_df['ClassDownUrg:Type'].str.contains("Furniture/Facilities", na=False)]

    choices = [
        "General Supplies Issue",
        "Furniture/Facilities Issue"
    ]

    crt_df['ClassDownUrg:Type'] = np.select(
        conditions,
        choices,
        default=crt_df['ClassDownUrg:Type']
    )

    # shorten down ctlm
    crt_df["Location"] = crt_df["Location"].str.replace("Center for Technology & Learning Media (CTLM)", "CTLM", regex=False)

    # fill na in location
    crt_df["Location"] = crt_df["Location"].fillna("Unknown")


    # counts = crt_df['Location'].value_counts()
    # ordered_locations = counts.index.tolist()
    # crt_df["Location"] = pd.Categorical(crt_df["Location"], categories=ordered_locations, ordered=True)

    CRT_ANNOTATIONS_SIZE = 14
    CRT_TITLE_SIZE = 20
    CRT_AXES_SIZE = 14

    START_DATE = pd.Timestamp("2025-08-01")
    END_DATE = pd.Timestamp("2026-01-31")

    BLASTER_BLUE = "#09396C"
    LIGHT_BLUE = "#879EC3"
    DARK_BLUE = "#21314d"
    COLORADO_RED = "#CC4628"

    crt_fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=["CRT Ticket Volumes", "Overall CRT Issues by Location", "Average CRT Ticket Resolution Times", "Overall CRT Issues Over Time"]
    )

    crt_fig.update_annotations(font_size=CRT_ANNOTATIONS_SIZE)

    # monthly volumms
    crt_df['Month'] = crt_df['Created'].dt.to_period('M').apply(lambda r: r.start_time)
    monthly_counts = crt_df.groupby('Month').size().reset_index(name="Ticket Count")

    # add text at top for total ticket count
    crt_count= len(crt_df)
    crt_fig.update_layout(
        title=dict(
            text=f"CRT: {crt_count} Tickets",
            x=0.45,
            y=0.98,
            xanchor="center",
            yanchor="top",
            font=dict(size=CRT_TITLE_SIZE)
        ),
        margin=dict(t=60)
    )


    # add monthly crt ticket volumes
    crt_df['Month'] = crt_df['Created'].dt.to_period('M').apply(lambda r: r.start_time)
    monthly_counts = crt_df.groupby('Month').size().reset_index(name="ticket_count")

    monthly_counts["pct_change"] = (monthly_counts["ticket_count"] - monthly_counts["ticket_count"].shift(1)) / monthly_counts["ticket_count"].shift(1) * 100
    end = END_DATE.replace(day=1)
    pct_change = monthly_counts.loc[monthly_counts["Month"] == end, "pct_change"].values[0]
    if pct_change < 0:
        change_text = f"{round(abs(pct_change), 1)} % decrease in ticket volumes compared to the previous month"
    elif pct_change > 0:
        change_text = f"{round(abs(pct_change), 1)} % increase in ticket volumes compared to the previous month"

    crt_fig.add_trace(
        go.Scatter(
            x=monthly_counts['Month'],
            y=monthly_counts['ticket_count'],
            mode='lines+markers',
            name='Monthly Ticket Volume',
            line=dict(color=BLASTER_BLUE, width=2),
            fill='tozeroy',
            showlegend=False
        ),
        row=1,
        col=1
    )
    crt_fig.update_xaxes(
        dtick="M1",
        tickformat="%b %Y",
        range=[START_DATE, END_DATE],
        title_font=dict(size=CRT_AXES_SIZE, color="black"),
        title_text="Months",
        row=1,
        col=1
    )
    crt_fig.update_yaxes(
        title_text="Ticket Counts", 
        row=1, 
        col=1,
        title_font=dict(size=CRT_AXES_SIZE, color="black")
    )


    # add crt buildings and issue types
    counts = crt_df['Location'].value_counts()

    fig = px.histogram(
        crt_df,
        x='Location',
        color='ClassDownUrg:Type',
        barmode="stack",
        title='CRT Tickets by Locations and Type',
        labels={'ClassDownUrg:Type': 'CRT Issue Type'}
    )

    fig.update_yaxes(title_text="Tickets")

    for i, trace in enumerate(fig.data):
        if trace.name == "General Supplies Issue":
            trace.marker.color = BLASTER_BLUE
        elif trace.name== "Furniture/Facilities Issue":
            trace.marker.color = COLORADO_RED
        elif trace.name == "AV / Computer/ Technology issue":
            trace.marker.color = LIGHT_BLUE

    for trace in fig.data:
        crt_fig.add_trace(trace, row=1, col=2)
    crt_fig.update_layout(barmode='stack')
    crt_fig.update_xaxes(
        tickfont=dict(size=CRT_AXES_SIZE - 2),
        row=1, col=2
    )
    crt_fig.update_yaxes(
        title_text="Ticket Counts", 
        row=1, 
        col=2,
        title_font=dict(size=CRT_AXES_SIZE, color="black")
    )


    # graph for mean crt response times
    monthly_response_times = crt_df.groupby('Month')["Create to Resolve (Abs) (No Hold)"].mean().reset_index(name="Mean Resolution Time")

    crt_fig.add_trace(
        go.Scatter(
            x=monthly_response_times['Month'],
            y=monthly_response_times["Mean Resolution Time"],
            mode='lines+markers',
            name='Mean Resolution Time',
            line=dict(color=DARK_BLUE, width=2),
            fill='tozeroy',
            showlegend=False
        ),
        row=2,
        col=1
    )

    crt_fig.update_xaxes(
        title_text="Months", 
        title_font=dict(size=CRT_AXES_SIZE, color="black"),
        dtick="M1",
        tickformat="%b %Y",
        range=[START_DATE, END_DATE],
        row=2,
        col=1
    )
    crt_fig.update_yaxes(
        title_text="Mean Resolution Times (Hrs)",
        title_font=dict(size=CRT_AXES_SIZE),
        row=2,
        col=1
    )


    # crt tickets by month and issues
    monthly_issues = crt_df.groupby(['Month', 'ClassDownUrg:Type']).size().reset_index(name="issue_count")
    monthly_pivot = monthly_issues.pivot(index='Month', columns='ClassDownUrg:Type', values='issue_count').fillna(0)

    color = None
    for i, issue_type in enumerate(monthly_pivot.columns):
        if issue_type == "General Supplies Issue":
            color = BLASTER_BLUE
        elif issue_type== "Furniture/Facilities Issue":
            color = COLORADO_RED
        elif issue_type == "AV / Computer/ Technology issue":
            color = LIGHT_BLUE
        crt_fig.add_trace(
            go.Bar(
                x=monthly_pivot.index,
                y=monthly_pivot[issue_type],
                name=issue_type,
                marker_color=color,
                showlegend=False
            ),
            row=2,
            col=2 
        )
    crt_fig.update_layout(barmode='stack')

    crt_fig.update_xaxes(
        title_text="Months",
        title_font=dict(size=CRT_AXES_SIZE),
        dtick="M1",
        tickformat="%b %Y",
        range=[START_DATE, END_DATE],
        row=2,
        col=2
    )
    crt_fig.update_yaxes(
        title_text="Ticket Counts",
        title_font=dict(size=CRT_AXES_SIZE),
        row=2,
        col=2
    )

    st.plotly_chart(crt_fig, width='stretch')

if __name__ == "__main__":
    main()
