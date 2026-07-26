import streamlit as st


def show_dashboard():

    st.title("🏭 Bhilai Steel Plant")

    st.subheader("Gate Pass Log Analyzer")

    st.divider()

    if "data" in st.session_state:

        df = st.session_state["data"]
        total_visitors = len(df)

    else:

        total_visitors = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Visitors", total_visitors)

    with col2:
        st.metric("Active Visitors", 0)

    with col3:
        st.metric("Today's Visitors", 0)

    with col4:
        st.metric("Completed Exits", 0)

    st.divider()

    if total_visitors == 0:
        st.info("Upload an Excel file to begin analysis.")