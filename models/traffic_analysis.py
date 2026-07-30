import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from Utils.prepocess import preprocess


def peak_hours(df):
    """Number of entries per hour of day (0-23), across all dates."""
    df = preprocess(df)

    traffic = (
        df.dropna(subset=["entry_hour"])
        .groupby("entry_hour")
        .size()
        .reset_index(name="Visitors")
        .rename(columns={"entry_hour": "Entry Hour"})
        .sort_values("Entry Hour")
    )

    return traffic


def gate_wise_traffic(df):
    """Returns visitor count for each gate."""
    gate_col = "Gate No" if "Gate No" in df.columns else "Gate Name"

    traffic = (
        df.groupby(gate_col)
        .size()
        .reset_index(name="Visitors")
        .sort_values("Visitors", ascending=False)
    )

    return traffic


def daily_traffic(df):
    """Returns daily visitor count using the real calendar date."""
    df = preprocess(df)

    traffic = (
        df.dropna(subset=["entry_date"])
        .groupby("entry_date")
        .size()
        .reset_index(name="Visitors")
        .rename(columns={"entry_date": "Entry Date"})
        .sort_values("Entry Date")
    )

    return traffic


def weekday_traffic(df):
    """Returns weekday-wise traffic."""
    df = preprocess(df)

    traffic = (
        df.dropna(subset=["entry_day"])
        .groupby("entry_day")
        .size()
        .reset_index(name="Visitors")
        .rename(columns={"entry_day": "Weekday"})
    )

    return traffic


def traffic_summary(df):
    """Returns basic traffic statistics."""
    df = preprocess(df)

    summary = {
        "Total Visitors": len(df),
        "Unique Visitors": df["Visitor Name"].nunique() if "Visitor Name" in df.columns else 0,
        "Total Gates": df["Gate No"].nunique() if "Gate No" in df.columns else 0,
        "Peak Hour": int(df["entry_hour"].mode().iloc[0]) if df["entry_hour"].notna().any() else None,
    }

    return summary


def forecast_daily_traffic(df, days_ahead=7):
    """
    Simple, explainable forecast: fits a straight-line trend (Linear
    Regression) through the historical daily visitor counts, then
    extends that line forward.

    This is intentionally simple (one feature: "day number") so it's
    easy to explain in a viva/evaluation -- it shows whether footfall
    is trending up, down, or flat, and gives a rough expected headcount
    for the next few days. It is NOT meant to be a production-grade
    time-series model.

    Returns:
        forecast_df : DataFrame with columns ['Date', 'Predicted Visitors']
        trend       : one of "increasing", "decreasing", "stable"
        r_squared   : how well the straight line fits the historical data
                      (0 to 1; closer to 1 = more reliable trend)
    """
    daily = daily_traffic(df)

    if len(daily) < 3:
        return pd.DataFrame(columns=["Date", "Predicted Visitors"]), "not enough data", None

    daily = daily.sort_values("Entry Date").reset_index(drop=True)
    daily["Day Number"] = np.arange(len(daily))

    X = daily[["Day Number"]].to_numpy()
    y = daily["Visitors"].to_numpy()

    model = LinearRegression()
    model.fit(X, y)
    r_squared = round(model.score(X, y), 3)

    last_day_number = daily["Day Number"].iloc[-1]
    last_date = pd.to_datetime(daily["Entry Date"].iloc[-1])

    future_day_numbers = np.arange(last_day_number + 1, last_day_number + 1 + days_ahead)
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, days_ahead + 1)]

    predictions = model.predict(future_day_numbers.reshape(-1, 1))
    predictions = np.clip(predictions, a_min=0, a_max=None).round().astype(int)

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted Visitors": predictions,
    })

    slope = model.coef_[0]
    if slope > 0.05:
        trend = "increasing"
    elif slope < -0.05:
        trend = "decreasing"
    else:
        trend = "stable"

    return forecast_df, trend, r_squared