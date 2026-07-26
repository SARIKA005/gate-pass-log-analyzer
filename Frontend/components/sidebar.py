import streamlit as st


def show_sidebar():

    page = st.sidebar.radio(

        "Navigation",

        [

            "🏠 Dashboard",

            "📂 Upload Excel",

            "📊 Gate-wise Analysis",

            "🚦 Peak Traffic",

            "🚪 Entry Exit",

            "🤖 AI Purpose",

            "⚠️ Anomaly Detection",

            "📄 Generate Report"

        ]

    )

    st.sidebar.divider()

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    return page