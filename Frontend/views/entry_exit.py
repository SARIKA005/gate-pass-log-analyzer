import streamlit as st
import pandas as pd


def show_entry_exit():

    st.title("🚪 Entry Exit Analysis")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"]

    total_entries = len(df)

    if "Exit Time" in df.columns:
        total_exits = df["Exit Time"].notna().sum()
    else:
        total_exits = 0

    inside = total_entries - total_exits

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Entries", total_entries)

    with col2:
        st.metric("Total Exits", total_exits)

    with col3:
        st.metric("Currently Inside", inside)

    st.divider()

    columns = [
        "Visitor Name",
        "Gate No",
        "Entry Time",
        "Exit Time"
    ]

    available_columns = [col for col in columns if col in df.columns]

    st.subheader("Visitor Entry & Exit Details")
    st.dataframe(df[available_columns], use_container_width=True)