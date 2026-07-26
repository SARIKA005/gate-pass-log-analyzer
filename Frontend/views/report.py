import streamlit as st
import pandas as pd


def show_report():

    st.title("📄 Analysis Report")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"].copy()

    # ==========================
    # Basic Statistics
    # ==========================

    total_visitors = len(df)

    total_gates = (
        df["Gate No"].nunique()
        if "Gate No" in df.columns
        else 0
    )

    total_purposes = (
        df["Purpose of Visit"].nunique()
        if "Purpose of Visit" in df.columns
        else 0
    )

    total_id_types = (
        df["ID Type"].nunique()
        if "ID Type" in df.columns
        else 0
    )

    if "Exit Time" in df.columns:
        total_exits = df["Exit Time"].notna().sum()
    else:
        total_exits = 0

    visitors_inside = total_visitors - total_exits

    # ==========================
    # Peak Hour
    # ==========================

    peak_hour = "N/A"

    if "Entry Time" in df.columns:

        try:

            temp = df.copy()

            temp["Entry Time"] = pd.to_datetime(
                temp["Entry Time"],
                format="%H:%M:%S",
                errors="coerce"
            )

            temp = temp.dropna(subset=["Entry Time"])

            if not temp.empty:

                temp["Hour"] = temp["Entry Time"].dt.strftime("%H:00")

                peak = temp["Hour"].value_counts().idxmax()

                peak_hour = peak

        except:
            pass

    # ==========================
    # KPI Cards
    # ==========================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("👥 Visitors", total_visitors)

    with c2:
        st.metric("🚪 Gates", total_gates)

    with c3:
        st.metric("🏢 Inside", visitors_inside)

    with c4:
        st.metric("⏰ Peak Hour", peak_hour)

    st.divider()

    # ==========================
    # Executive Summary
    # ==========================

    st.subheader("📝 Executive Summary")

    st.success(
        f"""
The uploaded dataset contains **{total_visitors} visitor records**
across **{total_gates} gates**.

There are **{total_purposes} different visit purposes**
and **{total_id_types} ID types**.

Currently **{visitors_inside} visitors** are inside the plant.

The busiest entry hour is **{peak_hour}**.
"""
    )

    st.divider()

    # ==========================
    # Gate-wise Summary
    # ==========================

    if "Gate No" in df.columns:

        st.subheader("🚪 Gate-wise Visitors")

        gate_summary = (
            df["Gate No"]
            .value_counts()
            .reset_index()
        )

        gate_summary.columns = [
            "Gate",
            "Visitors"
        ]

        st.dataframe(
            gate_summary,
            width="stretch"
        )

        st.bar_chart(
            gate_summary.set_index("Gate")
        )

    st.divider()

    # ==========================
    # Purpose Summary
    # ==========================

    if "Purpose of Visit" in df.columns:

        st.subheader("📋 Purpose Summary")

        purpose_summary = (
            df["Purpose of Visit"]
            .value_counts()
            .reset_index()
        )

        purpose_summary.columns = [
            "Purpose",
            "Visitors"
        ]

        st.dataframe(
            purpose_summary,
            width="stretch"
        )

    st.divider()

    st.subheader("📄 Complete Dataset")

    st.dataframe(
        df,
        width="stretch"
    )

    # ==========================
    # Download Report
    # ==========================

    st.divider()

    st.subheader("📥 Download Report")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Report (CSV)",
        data=csv,
        file_name="BSP_Gate_Pass_Report.csv",
        mime="text/csv"
    )