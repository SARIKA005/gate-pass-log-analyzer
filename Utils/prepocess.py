import pandas as pd


def preprocess(df):
    """
    Perform preprocessing and feature engineering.
    """

    df = df.copy()

    # Normalize column names for user-friendly display
    if "entry_time" in df.columns and "Entry Time" not in df.columns:
        df = df.rename(columns={"entry_time": "Entry Time"})
    if "exit_time" in df.columns and "Exit Time" not in df.columns:
        df = df.rename(columns={"exit_time": "Exit Time"})

    # Convert datetime columns
    df["Entry Time"] = pd.to_datetime(df["Entry Time"], errors="coerce")
    df["Exit Time"] = pd.to_datetime(df["Exit Time"], errors="coerce")

    # Entry features
    df["entry_hour"] = df["Entry Time"].dt.hour
    df["entry_day"] = df["Entry Time"].dt.day_name()
    df["entry_date"] = df["Entry Time"].dt.date
    df["entry_month"] = df["Entry Time"].dt.month_name()
    df["entry_year"] = df["Entry Time"].dt.year

    # Weekend flag
    df["is_weekend"] = df["Entry Time"].dt.dayofweek >= 5

    # Working hours flag (9 AM - 6 PM)
    df["working_hours"] = df["entry_hour"].between(9, 18)

    # Visit duration (minutes)
    df["visit_duration"] = (
        (df["Exit Time"] - df["Entry Time"])
        .dt.total_seconds() / 60
    )

    # Remove negative durations
    df.loc[df["visit_duration"] < 0, "visit_duration"] = None

    return df