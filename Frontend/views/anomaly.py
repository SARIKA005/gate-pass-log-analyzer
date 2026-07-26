import streamlit as st
import pandas as pd


def show_anomaly():

    st.title("⚠️ Anomaly Detection")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"].copy()

    # ==========================
    # Visitors Still Inside
    # ==========================

    if "Exit Time" in df.columns:
        inside_df = df[df["Exit Time"].isna()]
    else:
        inside_df = pd.DataFrame()

    # ==========================
    # Duplicate ID Numbers
    # ==========================

    if "ID No" in df.columns:
        duplicate_df = df[
            df["ID No"].duplicated(keep=False)
        ]
    else:
        duplicate_df = pd.DataFrame()

    # ==========================
    # Missing Information
    # ==========================

    important_columns = [
        "Visitor Name",
        "Gate No",
        "Purpose of Visit",
        "ID Type"
    ]

    existing_columns = [
        col
        for col in important_columns
        if col in df.columns
    ]

    if existing_columns:
        missing_df = df[
            df[existing_columns].isnull().any(axis=1)
        ]
    else:
        missing_df = pd.DataFrame()

    # ==========================
    # Total Unusual Records
    # ==========================

    total_anomalies = (
        len(inside_df)
        + len(duplicate_df)
        + len(missing_df)
    )

    # ==========================
    # KPI Cards
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "⚠️ Visitors Inside",
            len(inside_df)
        )

    with col2:
        st.metric(
            "🆔 Duplicate IDs",
            len(duplicate_df)
        )

    with col3:
        st.metric(
            "❌ Missing Records",
            len(missing_df)
        )

    with col4:
        st.metric(
            "🚨 Unusual Records",
            total_anomalies
        )

    st.divider()

    # ==========================
    # Visitors Still Inside
    # ==========================

    st.subheader("🚪 Visitors Still Inside")

    if inside_df.empty:
        st.success("✅ No visitors are currently inside.")
    else:
        st.dataframe(
            inside_df,
            width="stretch"
        )

    st.divider()

    # ==========================
    # Duplicate ID Numbers
    # ==========================

    st.subheader("🆔 Duplicate ID Numbers")

    if duplicate_df.empty:
        st.success("✅ No duplicate ID numbers found.")
    else:
        st.dataframe(
            duplicate_df,
            width="stretch"
        )

    st.divider()

    # ==========================
    # Missing Information
    # ==========================

    st.subheader("❌ Records with Missing Information")

    if missing_df.empty:
        st.success("✅ No missing information found.")
    else:
        st.dataframe(
            missing_df,
            width="stretch"
        )

    st.divider()

    # ==========================
    # Overall Status
    # ==========================

    if total_anomalies == 0:
        st.success("🎉 Great! No anomalies were detected in the uploaded dataset.")
    else:
        st.warning(
            f"⚠️ A total of {total_anomalies} unusual records were detected. "
            "Please review the tables above."
        )