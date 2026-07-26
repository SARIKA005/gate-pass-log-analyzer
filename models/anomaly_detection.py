import pandas as pd


def detect_anomalies(df):
    """
    Detect suspicious gate pass records based on simple rules.
    """

    df = df.copy()

    entry_col = "Entry Time" if "Entry Time" in df.columns else "entry_time"
    exit_col = "Exit Time" if "Exit Time" in df.columns else "exit_time"

    # Convert datetime columns
    df[entry_col] = pd.to_datetime(df[entry_col])
    df[exit_col] = pd.to_datetime(df[exit_col])

    anomalies = []

    for index, row in df.iterrows():

        reasons = []

        # Rule 1: Exit before entry
        if row[exit_col] < row[entry_col]:
            reasons.append("Exit before Entry")

        # Rule 2: Stay duration greater than 12 hours
        duration = (
            row[exit_col] - row[entry_col]
        ).total_seconds() / 3600

        if duration > 12:
            reasons.append("Long Stay (>12 hrs)")

        # Rule 3: Entry during late night
        if row[entry_col].hour >= 23 or row[entry_col].hour <= 4:
            reasons.append("Late Night Entry")

        # Rule 4: Missing purpose
        if pd.isna(row["Purpose of Visit"]) or str(row["Purpose of Visit"]).strip() == "":
            reasons.append("Missing Purpose")

        # Rule 5: Missing exit time
        if pd.isna(row[exit_col]):
            reasons.append("Missing Exit Time")

        if reasons:
            temp = row.copy()
            temp["Anomaly Reason"] = ", ".join(reasons)
            anomalies.append(temp)

    return pd.DataFrame(anomalies)