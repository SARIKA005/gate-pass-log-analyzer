import pandas as pd


def detect_anomalies(df):
    """
    Detect suspicious gate pass records based on simple rules.
    """

    df = df.copy()

    # Convert datetime columns
    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])

    anomalies = []

    for index, row in df.iterrows():

        reasons = []

        # Rule 1: Exit before entry
        if row["exit_time"] < row["entry_time"]:
            reasons.append("Exit before Entry")

        # Rule 2: Stay duration greater than 12 hours
        duration = (
            row["exit_time"] - row["entry_time"]
        ).total_seconds() / 3600

        if duration > 12:
            reasons.append("Long Stay (>12 hrs)")

        # Rule 3: Entry during late night
        if row["entry_time"].hour >= 23 or row["entry_time"].hour <= 4:
            reasons.append("Late Night Entry")

        # Rule 4: Missing purpose
        if pd.isna(row["Purpose of Visit"]) or str(row["Purpose of Visit"]).strip() == "":
            reasons.append("Missing Purpose")

        # Rule 5: Missing exit time
        if pd.isna(row["exit_time"]):
            reasons.append("Missing Exit Time")

        if reasons:
            temp = row.copy()
            temp["Anomaly Reason"] = ", ".join(reasons)
            anomalies.append(temp)

    return pd.DataFrame(anomalies)