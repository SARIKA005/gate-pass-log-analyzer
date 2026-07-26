import streamlit as st


def show_login():

    # ==========================
    # BSP Logo
    # ==========================
    st.image(
        "assets/bsp_logo.jpg",
        width=180
    )

    # ==========================
    # Project Title
    # ==========================
    st.title("🏭 Bhilai Steel Plant")
    st.caption("Steel Authority of India Limited (SAIL)")
    st.subheader("Gate Pass Log Analyzer")

    st.divider()

    st.write("Please login to continue")

    # ==========================
    # Login Form
    # ==========================
    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("🔐 Login"):

        if username == "admin" and password == "admin123":

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("❌ Invalid Username or Password")