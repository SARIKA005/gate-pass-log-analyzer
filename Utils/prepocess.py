
import pandas as pd


def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df


def preprocess(df):

    # Convert time columns
    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])

    # Create new features
    df["entry_hour"] = df["entry_time"].dt.hour
    df["exit_hour"] = df["exit_time"].dt.hour

    return df