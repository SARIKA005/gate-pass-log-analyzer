import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from views.login import show_login
from views.dashboard import show_dashboard
from views.upload import show_upload
from components.sidebar import show_sidebar
from views.gate_analysis import show_gate_analysis
from views.peak_traffic import show_peak_traffic
from views.entry_exit import show_entry_exit
from views.ai_purpose import show_ai_purpose
from views.vehicle_state import show as show_vehicle_state
from views.anomaly import show_anomaly
from views.report import show_report
# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(

    page_title="BSP Gate Pass Log Analyzer",

    page_icon="🏭",

    layout="wide"

)


# ----------------------------------
# Session State
# ----------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# ----------------------------------
# Main Application
# ----------------------------------

if not st.session_state.logged_in:

    show_login()

else:

    page = show_sidebar()

    if page == "🏠 Dashboard":

        show_dashboard()

    elif page == "📂 Upload Excel":

        show_upload()

    elif page == "📊 Gate-wise Analysis":

        show_gate_analysis()

    elif page == "🚦 Peak Traffic":

        show_peak_traffic() 

    elif page == "🚪 Entry Exit":

        show_entry_exit()

    elif page == "🤖 AI Purpose":

        show_ai_purpose()

    elif page == "🚗 Vehicle State Analysis":

        show_vehicle_state()

    elif page == "⚠️ Anomaly Detection":

        show_anomaly() 

    elif page == "📄 Generate Report":
        
        show_report()                    
    else:

        st.title(page)

        st.info("This module will be developed in the next step.")