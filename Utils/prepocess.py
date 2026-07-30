import pandas as pd


def _first_present(df, options):
    """Return the first column name from `options` that exists in df."""
    for name in options:
        if name in df.columns:
            return name
    return None


def preprocess(df):
    

    df = df.copy()

    date_col = _first_present(df, ["visit_date", "Visit Date", "visit date"])
    entry_col = _first_present(df, ["Entry Time", "entry_time"])
    exit_col = _first_present(df, ["Exit Time", "exit_time"])

    def combine(date_col, time_col):
        if time_col is None:
            return pd.Series(pd.NaT, index=df.index)
        if date_col is not None:
            base_date = pd.to_datetime(df[date_col], errors="coerce").dt.strftime("%Y-%m-%d")
            combined = base_date.fillna("") + " " + df[time_col].astype(str)
            return pd.to_datetime(combined, errors="coerce")
        # No separate date column available - fall back to parsing the
        # time column directly (all rows will share one placeholder date,
        # which is still fine for hour-of-day style aggregations).
        return pd.to_datetime(df[time_col], errors="coerce")

    df["Entry Datetime"] = combine(date_col, entry_col)
    df["Exit Datetime"] = combine(date_col, exit_col)

    # Time-based features
    df["entry_hour"] = df["Entry Datetime"].dt.hour
    df["entry_day"] = df["Entry Datetime"].dt.day_name()
    df["entry_date"] = df["Entry Datetime"].dt.date
    df["entry_month"] = df["Entry Datetime"].dt.month_name()
    df["entry_year"] = df["Entry Datetime"].dt.year
    df["is_weekend"] = df["Entry Datetime"].dt.dayofweek >= 5
    df["working_hours"] = df["entry_hour"].between(9, 18)

    # Visit duration in minutes. Negative values (exit logged before
    # entry) are kept as-is on purpose -- the anomaly detector uses
    # them to flag "Exit before Entry" as a data-quality issue instead
    # of silently hiding it.
    df["visit_duration_min"] = (
        (df["Exit Datetime"] - df["Entry Datetime"]).dt.total_seconds() / 60
    )

    return df


# Backward-compatible alias (older code / notebooks may import this name).
build_datetime_features = preprocess