import streamlit as st
import pandas as pd


def categorize_purpose(purpose):

    if pd.isna(purpose):
        return "Unknown"

    purpose = str(purpose).lower()

    if any(word in purpose for word in [
        "meeting",
        "inspection",
        "official",
        "audit",
        "review"
    ]):
        return "Official Visit"

    elif any(word in purpose for word in [
        "vendor",
        "delivery",
        "material",
        "supply"
    ]):
        return "Vendor"

    elif any(word in purpose for word in [
        "maintenance",
        "repair",
        "contract",
        "service"
    ]):
        return "Contractor"

    elif any(word in purpose for word in [
        "interview",
        "personal",
        "visitor",
        "guest"
    ]):
        return "Visitor"

    else:
        return "Other"


def show_ai_purpose():

    st.title("🤖 AI Purpose Categorization")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"].copy()

    if "Purpose of Visit" not in df.columns:
        st.error("Column 'Purpose of Visit' not found.")
        return

    # AI Categorization
    df["AI Category"] = df["Purpose of Visit"].apply(categorize_purpose)

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