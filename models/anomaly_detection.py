import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from Utils.prepocess import preprocess

LONG_STAY_HOURS = 12
IMPORTANT_COLUMNS = ["Visitor Name", "Gate No", "Purpose of Visit", "ID Type"]


def _is_blank(value):
    return pd.isna(value) or str(value).strip() == "" or str(value).strip().lower() == "nan"


def _rule_based_reasons(df):
    """
    Obvious, explainable checks -- each one is a clear policy / data
    quality violation that doesn't need any statistics to justify.
    """
    reasons = [[] for _ in range(len(df))]

    # Exit before entry
    bad_order = (
        df["Exit Datetime"].notna()
        & df["Entry Datetime"].notna()
        & (df["Exit Datetime"] < df["Entry Datetime"])
    )
    for i in np.where(bad_order)[0]:
        reasons[i].append("Exit before Entry")

    # Long stay
    long_stay = df["visit_duration_min"] > (LONG_STAY_HOURS * 60)
    for i in np.where(long_stay.fillna(False))[0]:
        reasons[i].append(f"Long Stay (>{LONG_STAY_HOURS} hrs)")

    # Late night entry (11 PM - 4 AM)
    late_night = df["entry_hour"].isin([23, 0, 1, 2, 3, 4])
    for i in np.where(late_night.fillna(False))[0]:
        reasons[i].append("Late Night Entry")

    # Missing purpose
    if "Purpose of Visit" in df.columns:
        missing_purpose = df["Purpose of Visit"].apply(_is_blank)
        for i in np.where(missing_purpose)[0]:
            reasons[i].append("Missing Purpose")

    # Still inside / missing exit time
    still_inside = df["Exit Datetime"].isna()
    for i in np.where(still_inside)[0]:
        reasons[i].append("Still Inside / Missing Exit Time")

    # Duplicate ID numbers
    if "ID No" in df.columns:
        dup_id = df["ID No"].duplicated(keep=False) & df["ID No"].notna()
        for i in np.where(dup_id)[0]:
            reasons[i].append("Duplicate ID Number")

    # Missing key info
    present_cols = [c for c in IMPORTANT_COLUMNS if c in df.columns]
    if present_cols:
        missing_info = df[present_cols].isna().any(axis=1)
        for i in np.where(missing_info.fillna(False))[0]:
            reasons[i].append("Missing Key Information")

    return [", ".join(r) for r in reasons]


def _ml_anomaly_scores(df, contamination=0.08):
    """
    ML layer: Isolation Forest looks at entry hour, visit duration and
    weekend flag TOGETHER and flags combinations that are statistically
    rare -- even when no single explicit rule fires. E.g. a 20-minute
    visit at 3 PM on a weekday is normal on its own, but a very short
    visit logged at an unusual hour on a weekend might stand out once
    the model has seen the overall pattern of the uploaded log.
    """
    
    duration = df["visit_duration_min"].where(df["visit_duration_min"] >= 0)
    upper_cap = duration.quantile(0.95)
    if pd.notna(upper_cap):
        duration = duration.clip(upper=upper_cap)

    features = pd.DataFrame({
        "entry_hour": df["entry_hour"],
        "visit_duration_min": duration,
        "is_weekend": df["is_weekend"].astype(float),
    })

    # Isolation Forest can't handle NaNs -- fill with the column median
    # so a few missing values don't block the whole model.
    features = features.fillna(features.median(numeric_only=True))

    if len(features) < 10 or features.nunique().sum() <= 3:
        # Not enough data (or no variation) for a meaningful model.
        return np.array([False] * len(df)), np.zeros(len(df))

    model = IsolationForest(contamination=contamination, random_state=42)
    predictions = model.fit_predict(features)          # -1 = anomaly, 1 = normal
    raw_scores = model.decision_function(features)      # lower = more anomalous

    flagged = predictions == -1
    # Flip sign so higher = more anomalous (more intuitive to read).
    anomaly_score = np.round(-raw_scores, 3)

    return flagged, anomaly_score


def detect_anomalies(df, contamination=0.08):
    """
    Runs both detection layers and returns the FULL dataframe annotated
    with:
      - 'Rule Reasons'     : comma-separated list of rule violations (or '')
      - 'ML Flagged'       : True if Isolation Forest thinks this row is
                             a statistical outlier
      - 'ML Anomaly Score' : higher = more unusual (0 if model couldn't run)
      - 'Is Anomaly'       : True if EITHER layer flagged the row

    Returning the full dataframe (not just the flagged rows) lets the
    dashboard show both "how many total records" and "how many flagged"
    KPIs from one call.
    """
    df = preprocess(df)

    df["Rule Reasons"] = _rule_based_reasons(df)
    df["Rule Flagged"] = df["Rule Reasons"] != ""

    ml_flagged, ml_scores = _ml_anomaly_scores(df, contamination=contamination)
    df["ML Flagged"] = ml_flagged
    df["ML Anomaly Score"] = ml_scores

    df["Is Anomaly"] = df["Rule Flagged"] | df["ML Flagged"]

    return df


def anomaly_summary(df):
    """Quick counts for KPI cards."""
    result = detect_anomalies(df)
    return {
        "Total Records": len(result),
        "Rule-Based Flags": int(result["Rule Flagged"].sum()),
        "ML-Detected Outliers": int(result["ML Flagged"].sum()),
        "Total Anomalies": int(result["Is Anomaly"].sum()),
    }