import streamlit as st 
uploaded_file = st.file_uploader("Upload Gate Pass Log", type=["xlsx"])
from utils.preprocess import load_data

df = load_data(uploaded_file)
import pandas as pd

def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df