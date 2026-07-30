import streamlit as st
import pandas as pd

from models.purpose_classifier import classify_dataframe


def show_ai_purpose():

    st.title("🤖 AI Purpose Categorization")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"].copy()

    if "Purpose of Visit" not in df.columns:
        st.error("Column 'Purpose of Visit' not found.")
        return

    # AI Categorization (semantic embeddings, not keyword matching)
    df = classify_dataframe(df, purpose_col="Purpose of Visit")
    df["AI Category"] = df["Purpose_Category"]

    category_count = (
        df["AI Category"]
        .value_counts()
        .reset_index()
    )

    category_count.columns = [
        "AI Category",
        "Visitors"
    ]

    # ==========================
    # KPI Cards
    # ==========================

    total_visitors = len(df)

    total_categories = category_count.shape[0]

    top_category = category_count.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👥 Total Visitors",
            total_visitors
        )

    with col2:
        st.metric(
            "📂 AI Categories",
            total_categories
        )

    with col3:
        st.metric(
            "🏆 Top Category",
            top_category["AI Category"]
        )

    st.divider()

    # ==========================
    # Summary Table
    # ==========================

    st.subheader("📋 AI Category Summary")

    st.dataframe(
        category_count,
        width="stretch"
    )

    st.divider()

    # ==========================
    # Bar Chart
    # ==========================

    st.subheader("📊 AI Category Distribution")

    st.bar_chart(
        category_count.set_index("AI Category")
    )

    st.divider()

    # ==========================
    # Detailed Records
    # ==========================

    st.subheader("📄 Visitor Categorization")

    columns = [
        "Visitor Name",
        "Purpose of Visit",
        "AI Category"
    ]

    available_columns = [
        col
        for col in columns
        if col in df.columns
    ]

    st.dataframe(
        df[available_columns],
        width="stretch"
    )

    st.success(
        f"✅ Most visitors belong to the '{top_category['AI Category']}' category."
    )