import streamlit as st
import pandas as pd


def show_anomaly():

    st.title("⚠️ Anomaly Detection")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"]

    anomaly_df = df[
        df["Entry Time"].isna()
        |
        df["Exit Time"].isna()
        |
        df["Vehicle Number"].isna()
        |
        df["ID No"].isna()
    ]

    st.metric("Anomalies Found", len(anomaly_df))

    st.divider()

    if len(anomaly_df) == 0:

        st.success("✅ No anomalies detected.")

    else:

        st.error(f"⚠️ {len(anomaly_df)} suspicious records found.")

        st.dataframe(
            anomaly_df,
            width="stretch"
        )