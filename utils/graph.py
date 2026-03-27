import plotly.express as px
import pandas as pd


def draw_ticket_volumes(df):
    # Add monthly ticket volumes
    df['Month'] = df['Created'].dt.to_period('M').apply(lambda r: r.start_time)
    monthly_counts = df.groupby('Month').size().reset_index(name="ticket_count")

    # Create full monthly range
    all_months = pd.date_range(
        start=df['Month'].min(),
        end=df['Month'].max(),
        freq='MS'
    )

    # Reindex to include missing months
    monthly_counts = (
        monthly_counts.set_index('Month')
        .reindex(all_months, fill_value=0)
        .rename_axis('Month')
        .reset_index()
    )

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
