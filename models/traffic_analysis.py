import pandas as pd


def preprocess_datetime(df):
    """
    Convert datetime columns and create useful time features.
    """

    df = df.copy()

    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])

    df["Entry Hour"] = df["entry_time"].dt.hour
    df["Entry Date"] = df["entry_time"].dt.date
    df["Weekday"] = df["entry_time"].dt.day_name()

    return df


def peak_hours(df):
    """
    Returns number of entries per hour.
    """

    df = preprocess_datetime(df)

    traffic = (
        df.groupby("Entry Hour")
        .size()
        .reset_index(name="Visitors")
        .sort_values("Entry Hour")
    )

    return traffic


def gate_wise_traffic(df):
    """
    Returns visitor count for each gate.
    """

    traffic = (
        df.groupby("Gate Name")
        .size()
        .reset_index(name="Visitors")
        .sort_values("Visitors", ascending=False)
    )

    return traffic


def daily_traffic(df):
    """
    Returns daily visitor count.
    """

    df = preprocess_datetime(df)

    traffic = (
        df.groupby("Entry Date")
        .size()
        .reset_index(name="Visitors")
    )

    return traffic


def weekday_traffic(df):
    """
    Returns weekday-wise traffic.
    """

    df = preprocess_datetime(df)

    traffic = (
        df.groupby("Weekday")
        .size()
        .reset_index(name="Visitors")
    )

    return traffic


def traffic_summary(df):
    """
    Returns basic traffic statistics.
    """

    df = preprocess_datetime(df)

    summary = {
        "Total Visitors": len(df),
        "Unique Visitors": df["Visitor Name"].nunique(),
        "Total Gates": df["Gate Name"].nunique(),
        "Peak Hour": df["Entry Hour"].mode()[0],
        "Busiest Gate": df["Gate Name"].mode()[0]
    }

    return summary