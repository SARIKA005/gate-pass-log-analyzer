import streamlit as st
import pandas as pd

from models.traffic_analysis import forecast_daily_traffic


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

        st.divider()

        # ==========================
        # AI Traffic Forecast (Linear Regression)
        # ==========================

        st.subheader("📈 AI Traffic Forecast — Next 7 Days")
        st.caption(
            "A Linear Regression model fits a straight-line trend through the "
            "historical daily visitor counts and extends it forward. Simple by "
            "design so the trend is easy to read and explain."
        )

        forecast_df, trend, r_squared = forecast_daily_traffic(
            st.session_state["data"], days_ahead=7
        )

        if forecast_df.empty:
            st.info(
                "Not enough distinct dates in this dataset yet to fit a reliable "
                "trend (need at least 3 different visit dates)."
            )
        else:
            trend_label = {
                "increasing": "📈 Increasing",
                "decreasing": "📉 Decreasing",
                "stable": "➡️ Stable",
            }.get(trend, trend)

            fcol1, fcol2 = st.columns(2)

            with fcol1:
                st.metric("Footfall Trend", trend_label)

            with fcol2:
                st.metric("Model Fit (R²)", r_squared)

            st.dataframe(
                forecast_df,
                width="stretch"
            )

            st.line_chart(
                forecast_df.set_index("Date")["Predicted Visitors"]
            )

    except Exception as e:
        st.error(f"Error: {e}")