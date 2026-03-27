import plotly.express as px
import pandas as pd


def draw_ticket_volumes(df):
    # add monthly ticket volumes
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
    fig.update_traces(fill='tozeroy')
    fig.update_layout(
        title_x=0.5,
        title_xanchor='center',
        title_font=dict(size=20),
        paper_bgcolor='rgba(0,0,0,0)', # Transparent background
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
    )
    return fig