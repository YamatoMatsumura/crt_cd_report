from pathlib import Path
import pandas as pd
import numpy as np

def load_cd_data():

    excel_folder_path = Path("data/")

    classroom_down_path = None
    for item in excel_folder_path.iterdir():
        if item.is_file():
            if "Classroom Downs Report" in item.name:
                classroom_down_path = f"{excel_folder_path}/{item.name}"

    cd_df = pd.read_excel(classroom_down_path)
    return cd_df

def parse_cd_data(cd_df):

    # Create unique building and room names
    cd_df["Location"] = cd_df["Location"].str.replace("Center for Technology & Learning Media (CTLM)", "CTLM", regex=False)
    cd_df["room_names"] = cd_df['Location'].astype(str) + " " + cd_df['Location Room'].astype(str)
    cd_df['Created'] = pd.to_datetime(cd_df['Created'])

    return cd_df

def load_crt_data():

    excel_folder_path = Path("data")

    crt_path = None
    for item in excel_folder_path.iterdir():
        if item.is_file():
            if "CRT Tickets" in item.name:
                crt_path = f"{excel_folder_path}/{item.name}"

    crt_df = pd.read_excel(crt_path)
    return crt_df

def parse_crt_data(crt_df):

    # Rename classroom down types for clarity
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
    return crt_df

def get_monthly_agg(df):
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

    return monthly_counts