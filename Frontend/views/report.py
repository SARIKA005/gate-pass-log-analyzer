import streamlit as st
import pandas as pd


def show_report():

    st.title("📄 Generate Report")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"]

    st.subheader("📋 Analysis Summary")

    total_visitors = len(df)

    total_gates = df["Gate No"].nunique()

    most_used_gate = df["Gate No"].mode()[0]

    most_common_purpose = df["Purpose of Visit"].mode()[0]

    summary = pd.DataFrame({

        "Metric": [
            "Total Visitors",
            "Total Gates",
            "Most Used Gate",
            "Most Common Purpose"
        ],

        "Value": [
            total_visitors,
            total_gates,
            most_used_gate,
            most_common_purpose
        ]

    })

    st.dataframe(summary, use_container_width=True)

    st.divider()

    st.subheader("⬇️ Download Complete Gate Pass Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="📥 Download CSV Report",

        data=csv,

        file_name="GatePass_Report.csv",

        mime="text/csv"

    )

    st.success("✅ Report is ready for download.")