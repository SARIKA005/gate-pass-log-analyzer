import pandas as pd
import streamlit as st


def check_required_columns(df, required_columns):
    """
    Check if all required columns are present.

    Parameters:
        df (DataFrame)
        required_columns (list)

    Returns:
        bool
    """
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        return False

    return True


def format_number(number):
    """
    Format large numbers with commas.

    Example:
        1000 -> 1,000
    """
    return f"{number:,}"


def safe_datetime(value):
    """
    Safely convert value to datetime.
    Returns NaT if conversion fails.
    """
    return pd.to_datetime(value, errors="coerce")


def safe_string(value):
    """
    Convert value to clean string.
    """
    if pd.isna(value):
        return ""

    return str(value).strip()


def percentage(part, whole):
    """
    Calculate percentage.
    """
    if whole == 0:
        return 0

    return round((part / whole) * 100, 2)


def download_dataframe(df, filename="report.csv"):
    """
    Streamlit CSV download button.
    """
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )