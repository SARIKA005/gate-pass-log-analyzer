import streamlit as st
import pandas as pd


def show_entry_exit():

    st.title("🚪 Entry & Exit Analysis")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"].copy()

    total_entries = len(df)

    # Count exits
    if "Exit Time" in df.columns:
        total_exits = df["Exit Time"].notna().sum()
    else:
        total_exits = 0

    currently_inside = total_entries - total_exits

    completion_rate = (
        (total_exits / total_entries) * 100
        if total_entries > 0
        else 0
    )

    # ==========================
    # KPI Cards
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Entries", total_entries)

    with col2:
        st.metric("🚪 Total Exits", total_exits)

    with col3:
        st.metric("🏢 Currently Inside", currently_inside)

    with col4:
        st.metric("✅ Exit Completion", f"{completion_rate:.1f}%")

    st.divider()

    # ==========================
    # Entry vs Exit Chart
    # ==========================

    st.subheader("📊 Entry vs Exit Comparison")

    chart_data = pd.DataFrame(
        {
            "Count": [
                total_entries,
                total_exits,
                currently_inside
            ]
        },
        index=[
            "Entries",
            "Exits",
            "Inside"
        ]
    )

    st.bar_chart(chart_data)

    st.divider()

    # ==========================
    # Visitor Details
    # ==========================

    columns = [
        "Visitor Name",
        "Gate No",
        "Entry Time",
        "Exit Time"
    ]

    available_columns = [
        col
        for col in columns
        if col in df.columns
    ]

    st.subheader("📄 Visitor Entry & Exit Details")

    st.dataframe(
        df[available_columns],
        width="stretch"
    )

    st.divider()

    # ==========================
    # Visitors Still Inside
    # ==========================

    if "Exit Time" in df.columns:

        inside_df = df[df["Exit Time"].isna()]

        if not inside_df.empty:

            st.subheader("⚠️ Visitors Currently Inside")

            st.dataframe(
                inside_df[available_columns],
                width="stretch"
            )

        else:

            st.success("✅ All visitors have exited.")