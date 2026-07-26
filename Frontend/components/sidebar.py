import streamlit as st


def show_sidebar():

    # ==========================
    # BSP Logo
    # ==========================
    st.sidebar.image(
        "assets/bsp_logo.jpg",
        width="stretch"
    )

    # ==========================
    # Project Title
    # ==========================
    st.sidebar.markdown("## 🏭 Bhilai Steel Plant")
    st.sidebar.caption("Steel Authority of India Limited (SAIL)")
    st.sidebar.markdown("### Gate Pass Log Analyzer")

    st.sidebar.divider()

    # ==========================
    # Navigation
    # ==========================
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

    # ==========================
    # Logout Button
    # ==========================
    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.rerun()

    return page