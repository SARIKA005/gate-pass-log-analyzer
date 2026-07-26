import streamlit as st
import pandas as pd


def show_ai_purpose():

    st.title("🤖 AI Purpose Analysis")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"]

    if "Purpose of Visit" not in df.columns:
        st.error("Column 'Purpose of Visit' not found.")
        return

    purpose_count = (
        df["Purpose of Visit"]
        .value_counts()
    )

    st.subheader("Purpose-wise Visitor Count")

    st.dataframe(
        purpose_count.reset_index().rename(
            columns={
                "index": "Purpose of Visit",
                "Purpose of Visit": "Visitors"
            }
        ),
        width="stretch"
    )

    st.subheader("📊 Purpose Distribution")

    st.bar_chart(purpose_count)

    most_common = purpose_count.idxmax()
    total = purpose_count.max()

    st.success(
        f"🏆 Most Common Purpose: {most_common} ({total} Visitors)"
    )