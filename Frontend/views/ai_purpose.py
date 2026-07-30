import streamlit as st
import pandas as pd

from models.purpose_classifier import classify_dataframe, analyze_other_cluster


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

    avg_confidence = round(df["Category_Confidence"].mean(), 3)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Total Visitors",
            total_visitors
        )

    with col2:
        st.metric(
            "📂Categories",
            total_categories
        )

    with col3:
        st.metric(
            "🏆 Top Category",
            top_category["AI Category"]
        )

    with col4:
        st.metric(
            "🎯 Avg. Confidence",
            avg_confidence
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
        "AI Category",
        "Category_Confidence"
    ]

    available_columns = [
        col
        for col in columns
        if col in df.columns
    ]

    display_df = df[available_columns].rename(
        columns={"Category_Confidence": "Confidence"}
    )

    st.dataframe(
        display_df,
        width="stretch"
    )

    st.caption(
        f"Confidence is the cosine-similarity score (0–1) between a visitor's stated "
        f"purpose and the closest category description. Anything below "
        f"**{0.35}** gets bucketed as 'Other' instead of being force-fit into a wrong category."
    )

    st.success(
        f"✅ Most visitors belong to the '{top_category['AI Category']}' category."
    )

    st.divider()

    # ==========================
    # Auto-Discover New Categories from "Other"
    # ==========================

    st.subheader("🔍 Discover Hidden Patterns in 'Other'")
    st.caption(
        "Whatever didn't match an existing category gets grouped with KMeans "
        "clustering, so you can spot a new recurring purpose (e.g. 'Bill Payment' "
        "or 'RTI Query') that the fixed category list doesn't cover yet."
    )

    other_count = int((df["AI Category"] == "Other").sum())

    if other_count < 5:
        st.info(
            f"Only {other_count} record(s) fell into 'Other' — need at least 5 "
            "to form meaningful clusters."
        )
    else:
        n_clusters = min(5, other_count // 2) or 1
        clustered = analyze_other_cluster(
            df, purpose_col="Purpose of Visit", n_clusters=n_clusters
        )

        for cluster_id in sorted(clustered["Cluster"].unique()):
            cluster_rows = clustered[clustered["Cluster"] == cluster_id]
            samples = cluster_rows["Purpose of Visit"].head(3).tolist()

            with st.expander(f"Cluster {cluster_id} — {len(cluster_rows)} visitor(s)"):
                for sample in samples:
                    st.write(f"• {sample}")