import streamlit as st
import pandas as pd


def show_gate_analysis():

    st.title("📊 Gate-wise Analysis")

    if "data" not in st.session_state:

        st.warning("Please upload an Excel file first.")

        return

    df = st.session_state.data

    st.subheader("Visitors by Gate")

    gate_count = (
        df["Gate No"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    gate_count.columns = ["Gate No", "Visitors"]

    st.dataframe(gate_count, width="stretch")