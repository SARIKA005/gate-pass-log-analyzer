import pandas as pd


def preprocess(df):
    """
    Perform preprocessing and feature engineering.
    """

    df = df.copy()

    # Convert datetime columns
    df["entry_time"] = pd.to_datetime(df["entry_time"], errors="coerce")
    df["exit_time"] = pd.to_datetime(df["exit_time"], errors="coerce")

    # Entry features
    df["entry_hour"] = df["entry_time"].dt.hour
    df["entry_day"] = df["entry_time"].dt.day_name()
    df["entry_date"] = df["entry_time"].dt.date
    df["entry_month"] = df["entry_time"].dt.month_name()
    df["entry_year"] = df["entry_time"].dt.year

    # Weekend flag
    df["is_weekend"] = df["entry_time"].dt.dayofweek >= 5

    # Working hours flag (9 AM - 6 PM)
    df["working_hours"] = df["entry_hour"].between(9, 18)

    # Visit duration (minutes)
    df["visit_duration"] = (
        (df["exit_time"] - df["entry_time"])
        .dt.total_seconds() / 60
    )

    # Remove negative durations
    df.loc[df["visit_duration"] < 0, "visit_duration"] = None

    return df