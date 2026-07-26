import streamlit as st


def show_login():

    st.title("🏭 Bhilai Steel Plant")

    st.subheader("Gate Pass Log Analyzer")

    st.write("Please login to continue")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "admin123":

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("Invalid Username or Password")