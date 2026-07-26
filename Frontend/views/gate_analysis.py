import streamlit as st
import pandas as pd


def show_gate_analysis():

    st.title("📊 Gate-wise Analysis")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state.data

    st.subheader("Visitors by Gate")

    df.columns = df.columns.str.strip()

    if "Gate No" not in df.columns:
        st.error(f"'Gate No' column not found.\nAvailable columns: {list(df.columns)}")
        st.stop()

    gate_count = (
        df["Gate No"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    gate_count.columns = ["Gate No", "Visitors"]

    st.dataframe(gate_count, width="stretch")