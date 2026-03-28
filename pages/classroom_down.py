from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import streamlit as st

import utils.data as data 

def main():
    cd_df = data.load_cd_data()
    cd_df = data.parse_cd_data(cd_df)

    st.title("Classroom Down Dashboard")

    CD_ANNOTATIONS_SIZE = 15
    CD_TITLE_SIZE = 20
    CD_AXES_SIZE = 14

    # TODAY = str(datetime.today().date())

    import plotly.express as px
    from datetime import datetime

    START_DATE = pd.Timestamp("2025-08-01")
    END_DATE = pd.Timestamp("2026-01-31")

    BLASTER_BLUE = "#09396C"
    LIGHT_BLUE = "#879EC3"
    DARK_BLUE = "#21314d"
    COLORADO_RED = "#CC4628"


    cd_fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Monthly Classroom Down Ticket Volumes", "Monthly Classroom Down Average Resolution Times"]
    )

    cd_fig.update_annotations(font_size=CD_ANNOTATIONS_SIZE)

    # add text at top for total ticket count
    cd_count = len(cd_df)
    cd_fig.update_layout(
        title=dict(
            text=f"Classroom Downs: {cd_count} Tickets",
            x=0.5,
            y=0.98,
            xanchor="center",
            yanchor="top",
            font=dict(size=CD_TITLE_SIZE)
        ),
        margin=dict(t=60)
    )


    # add monthly ticket volumes
    cd_df['Month'] = cd_df['Created'].dt.to_period('M').apply(lambda r: r.start_time)
    monthly_counts = cd_df.groupby('Month').size().reset_index(name="ticket_count")

    monthly_counts["pct_change"] = (monthly_counts["ticket_count"] - monthly_counts["ticket_count"].shift(1)) / monthly_counts["ticket_count"].shift(1) * 100
    end = END_DATE.replace(day=1)
    pct_change = monthly_counts.loc[monthly_counts["Month"] == end, "pct_change"].values[0]
    if pct_change < 0:
        change_text = f"{round(abs(pct_change), 1)} % decrease in ticket volumes compared to the previous month"
    elif pct_change > 0:
        change_text = f"{round(abs(pct_change), 1)} % increase in ticket volumes compared to the previous month"

    cd_fig.add_trace(
        go.Scatter(
            x=monthly_counts['Month'],
            y=monthly_counts['ticket_count'],
            mode='lines+markers',
            name='Monthly Ticket Volume',
            line=dict(color=BLASTER_BLUE, width=2),
            fill='tozeroy'
        ),
        row=1,
        col=1
    )
    cd_fig.update_xaxes(
        dtick="M1",
        tickformat="%b %Y",
        range=[START_DATE, END_DATE],
        title_text="Months", 
        title_font=dict(size=CD_AXES_SIZE, color="black"),
        row=1,
        col=1
    )
    cd_fig.update_yaxes(
        title_text="Ticket Counts", 
        row=1, 
        col=1,
        title_font=dict(size=CD_AXES_SIZE, color="black")
    )


    # add monthly ticket response times
    # cd_df["Create to Resolve (Abs) (No Hold)"].hist(bins=30)
    lower = cd_df["Create to Resolve (Abs) (No Hold)"].quantile(0.01)
    upper = cd_df["Create to Resolve (Abs) (No Hold)"].quantile(0.99)
    filtered_cd_df = cd_df[(cd_df["Create to Resolve (Abs) (No Hold)"] >= lower) & (cd_df["Create to Resolve (Abs) (No Hold)"] <= upper)]

    monthly_response_times = cd_df.groupby('Month')["Create to Resolve (Abs) (No Hold)"].mean().reset_index(name="Mean Resolution Time")

    cd_fig.add_trace(
        go.Scatter(
            x=monthly_response_times['Month'],
            y=monthly_response_times["Mean Resolution Time"],
            mode='lines+markers',
            name='Mean Resolution Time',
            line=dict(color=DARK_BLUE, width=2),
            fill='tozeroy'
        ),
        row=1,
        col=2
    )

    cd_fig.update_xaxes(
        title_text="Months", 
        title_font=dict(size=CD_AXES_SIZE, color="black"),
        dtick="M1",
        tickformat="%b %Y",
        range=[START_DATE, END_DATE],
        row=1,
        col=2
    )
    cd_fig.update_yaxes(
        title_text="Mean Resolution Times (Hrs)",
        title_font=dict(size=CD_AXES_SIZE),
        row=1,
        col=2
    )

    cd_fig.update_layout(showlegend=False)
    st.plotly_chart(cd_fig, width='stretch')

if __name__ == "__main__":
    main()