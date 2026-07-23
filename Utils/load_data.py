import pandas as pd
import streamlit as st


def load_excel(uploaded_file):
    

    try:
        df = pd.read_excel(uploaded_file)

        if df.empty:
            st.error("The uploaded Excel file is empty.")
            return None

        return df

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None