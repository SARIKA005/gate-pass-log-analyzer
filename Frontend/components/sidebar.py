import streamlit as st
from pathlib import Path


def show_sidebar():

    # ==========================
    # BSP Logo
    # ==========================
    BASE_DIR = Path(__file__).resolve().parent.parent
    logo_path = BASE_DIR / "assets" / "bsp_logo.jpg"

    st.sidebar.image(
        str(logo_path),
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

            "🚗 Vehicle State Analysis",

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