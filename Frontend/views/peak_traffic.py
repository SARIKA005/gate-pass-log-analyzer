import streamlit as st
import pandas as pd


def show_peak_traffic():

    st.title("🚦 Peak Traffic Detection")

    if "data" not in st.session_state:

        st.warning("Please upload an Excel file first.")

        return

    df = st.session_state["data"]

    if "Entry Time" not in df.columns:

        st.error("Column 'Entry Time' not found.")

        return

    # Convert Entry Time to datetime
    df["Entry Time"] = pd.to_datetime(
        df["Entry Time"],
        format="%H:%M:%S"
    )

    # Extract Hour
    df["Hour"] = df["Entry Time"].dt.strftime("%H:00")

    hour_count = (
        df["Hour"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    hour_count.columns = ["Hour", "Visitors"]

    st.subheader("Visitors by Hour")

    st.dataframe(hour_count, use_container_width=True)

    st.subheader("Peak Traffic Chart")

    st.bar_chart(
        hour_count.set_index("Hour")
    )

    peak = hour_count.loc[
        hour_count["Visitors"].idxmax()
    ]

    st.success(
        f"🏆 Peak Traffic Hour : {peak['Hour']} ({peak['Visitors']} Visitors)"
    )