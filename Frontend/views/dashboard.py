import streamlit as st
import pandas as pd


def show_dashboard():

    st.title("🏭 Bhilai Steel Plant")
    st.subheader("Gate Pass Log Analyzer")
    st.divider()

    if "data" not in st.session_state:
        st.info("📂 Upload an Excel file to begin analysis.")
        return

    df = st.session_state["data"]

    # ==========================
    # KPI Metrics
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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Visitors", total_visitors)

    with col2:
        st.metric("🚪 Total Gates", total_gates)

    with col3:
        st.metric("📋 Visit Purposes", total_purposes)

    with col4:
        st.metric("🆔 ID Types", total_id_types)

    st.divider()

    # ==========================
    # Gate-wise Analysis
    # ==========================

    if "Gate No" in df.columns:

        st.subheader("🚪 Gate-wise Visitor Analysis")

        gate_count = df["Gate No"].value_counts()

        st.bar_chart(gate_count)

    st.divider()

    # ==========================
    # Purpose-wise Analysis
    # ==========================

    if "Purpose of Visit" in df.columns:

        st.subheader("📋 Purpose-wise Visitor Analysis")

        purpose_count = df["Purpose of Visit"].value_counts()

        st.bar_chart(purpose_count)

    st.divider()

    # ==========================
    # ID Type Analysis
    # ==========================

    if "ID Type" in df.columns:

        st.subheader("🆔 ID Type Distribution")

        id_count = df["ID Type"].value_counts()

        st.bar_chart(id_count)

    st.divider()

    # ==========================
    # Preview
    # ==========================

    st.subheader("📄 Uploaded Data Preview")

    st.dataframe(
        df,
        width="stretch"
    )