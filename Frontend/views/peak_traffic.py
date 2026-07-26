import streamlit as st
import pandas as pd


def show_peak_traffic():

    st.title("🚦 Peak Traffic Detection")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"].copy()

    if "Entry Time" not in df.columns:
        st.error("Column 'Entry Time' not found.")
        return

    try:
        # Convert Entry Time
        df["Entry Time"] = pd.to_datetime(
            df["Entry Time"],
            format="%H:%M:%S",
            errors="coerce"
        )

        df = df.dropna(subset=["Entry Time"])

        # Extract Hour
        df["Hour"] = df["Entry Time"].dt.strftime("%H:00")

        hour_count = (
            df["Hour"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        hour_count.columns = ["Hour", "Visitors"]

        # ==========================
        # KPI Cards
        # ==========================

        peak = hour_count.loc[
            hour_count["Visitors"].idxmax()
        ]

        total_entries = hour_count["Visitors"].sum()

        avg_entries = round(
            hour_count["Visitors"].mean(),
            1
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🏆 Peak Hour",
                peak["Hour"]
            )

        with col2:
            st.metric(
                "👥 Peak Visitors",
                peak["Visitors"]
            )

        with col3:
            st.metric(
                "📊 Avg Visitors / Hour",
                avg_entries
            )

        st.divider()

        st.subheader("📋 Hour-wise Visitor Summary")

        st.dataframe(
            hour_count,
            width="stretch"
        )

        st.divider()

        st.subheader("📊 Hour-wise Traffic Chart")

        st.bar_chart(
            hour_count.set_index("Hour")
        )

        st.success(
            f"🚦 Highest traffic was recorded at **{peak['Hour']}** with **{peak['Visitors']} visitors**."
        )

    except Exception as e:
        st.error(f"Error: {e}")