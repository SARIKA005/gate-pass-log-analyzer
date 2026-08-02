import streamlit as st
import pandas as pd


def show_report():

    st.title("📄 Analysis Report")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"].copy()

    # ==========================
    # Basic Statistics
    # ==========================

    total_visitors = len(df)

    total_gates = (
        df["Gate No"].nunique()
        if "Gate No" in df.columns
        else 0
    )

    total_purposes = (
        df["Purpose of Visit"].nunique()
        if "Purpose of Visit" in df.columns
        else 0
    )

    total_id_types = (
        df["ID Type"].nunique()
        if "ID Type" in df.columns
        else 0
    )

    if "Exit Time" in df.columns:
        total_exits = df["Exit Time"].notna().sum()
    else:
        total_exits = 0

    visitors_inside = total_visitors - total_exits

    # ==========================
    # Peak Hour
    # ==========================

    peak_hour = "N/A"

    if "Entry Time" in df.columns:

        try:

            temp = df.copy()

            temp["Entry Time"] = pd.to_datetime(
                temp["Entry Time"],
                format="%H:%M:%S",
                errors="coerce"
            )

            temp = temp.dropna(subset=["Entry Time"])

            if not temp.empty:

                temp["Hour"] = temp["Entry Time"].dt.strftime("%H:00")

                peak = temp["Hour"].value_counts().idxmax()

                peak_hour = peak

        except:
            pass

    # ==========================
    # KPI Cards
    # ==========================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("👥 Visitors", total_visitors)

    with c2:
        st.metric("🚪 Gates", total_gates)

    with c3:
        st.metric("🏢 Inside", visitors_inside)

    with c4:
        st.metric("⏰ Peak Hour", peak_hour)

    st.divider()

    # ==========================
    # Executive Summary
    # ==========================

    st.subheader("📝 Executive Summary")

    st.success(
        f"""
The uploaded dataset contains **{total_visitors} visitor records**
across **{total_gates} gates**.

There are **{total_purposes} different visit purposes**
and **{total_id_types} ID types**.

Currently **{visitors_inside} visitors** are inside the plant.

The busiest entry hour is **{peak_hour}**.
"""
    )

    st.divider()

    # ==========================
    # Gate-wise Summary
    # ==========================

    if "Gate No" in df.columns:

        st.subheader("🚪 Gate-wise Visitors")

        gate_summary = (
            df["Gate No"]
            .value_counts()
            .reset_index()
        )

        gate_summary.columns = [
            "Gate",
            "Visitors"
        ]

        st.dataframe(
            gate_summary,
            width="stretch"
        )

        st.bar_chart(
            gate_summary.set_index("Gate")
        )

    st.divider()

    # ==========================
    # Purpose Summary
    # ==========================

    if "Purpose of Visit" in df.columns:

        st.subheader("📋 Purpose Summary")

        purpose_summary = (
            df["Purpose of Visit"]
            .value_counts()
            .reset_index()
        )

        purpose_summary.columns = [
            "Purpose",
            "Visitors"
        ]

        st.dataframe(
            purpose_summary,
            width="stretch"
        )

    st.divider()

    st.subheader("📄 Complete Dataset")

    st.dataframe(
    df,
    width="stretch"
    )

    # ==========================
    # Download Report
    # ==========================
    st.divider()
    st.subheader("📥 Download Analysis Report")

    report = []

    # Header
    report.append(["BSP GATE PASS LOG ANALYZER", ""])
    report.append(["Steel Authority of India Limited (SAIL)", ""])
    report.append(["ANALYSIS REPORT", ""])
    report.append(["", ""])

    # Executive Summary
    report.append(["Executive Summary", ""])
    report.append(["Total Visitors", total_visitors])
    report.append(["Total Gates", total_gates])
    report.append(["Visitors Inside", visitors_inside])
    report.append(["Completed Exits", total_exits])
    report.append(["Peak Traffic Hour", peak_hour])
    report.append(["Total Visit Purposes", total_purposes])
    report.append(["Total ID Types", total_id_types])

    # Vehicle State Summary
    if "Vehicle_no" in df.columns:

        state_codes = {
            "AP":"Andhra Pradesh","AR":"Arunachal Pradesh","AS":"Assam",
            "BR":"Bihar","CG":"Chhattisgarh","CH":"Chandigarh",
            "DL":"Delhi","GA":"Goa","GJ":"Gujarat",
            "HR":"Haryana","HP":"Himachal Pradesh",
            "JH":"Jharkhand","JK":"Jammu & Kashmir",
            "KA":"Karnataka","KL":"Kerala","LA":"Ladakh",
            "MH":"Maharashtra","ML":"Meghalaya","MN":"Manipur",
            "MP":"Madhya Pradesh","MZ":"Mizoram","NL":"Nagaland",
            "OD":"Odisha","PB":"Punjab","PY":"Puducherry",
            "RJ":"Rajasthan","SK":"Sikkim","TN":"Tamil Nadu",
            "TR":"Tripura","TS":"Telangana","UK":"Uttarakhand",
            "UP":"Uttar Pradesh","WB":"West Bengal"
        }

        vehicles = (
            df["Vehicle_no"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.strip()
        )

        valid_states = []
        invalid = 0

        for vehicle in vehicles:

            if len(vehicle) < 2:
                invalid += 1
                continue

            code = vehicle[:2]

            if code in state_codes:
                valid_states.append(state_codes[code])
            else:
                invalid += 1

        if valid_states:

            state_summary = (
                pd.Series(valid_states)
                .value_counts()
                .reset_index()
            )

            state_summary.columns = ["State", "Vehicles"]

            report.append(["", ""])
            report.append(["Vehicle State Summary", ""])
            report.append(["Valid Vehicle Numbers", len(valid_states)])
            report.append(["Invalid Vehicle Numbers", invalid])
            report.append(["Total States Represented", len(state_summary)])
            report.append(["Top State", state_summary.iloc[0]["State"]])

            report.append(["", ""])
            report.append(["Top 5 States", ""])
            report.append(["State", "Vehicles"])

            for _, row in state_summary.head(5).iterrows():
                report.append([row["State"], row["Vehicles"]])

    # Gate Summary
    if "Gate No" in df.columns:

        report.append(["", ""])
        report.append(["Gate-wise Summary", ""])
        report.append(["Gate", "Visitors"])

        gate_summary = (
            df["Gate No"]
            .value_counts()
            .reset_index()
        )

        gate_summary.columns = ["Gate", "Visitors"]

        for _, row in gate_summary.iterrows():
            report.append([row["Gate"], row["Visitors"]])

    # Purpose Summary
    if "Purpose of Visit" in df.columns:

        report.append(["", ""])
        report.append(["Purpose Summary", ""])
        report.append(["Purpose", "Visitors"])

        purpose_summary = (
            df["Purpose of Visit"]
            .value_counts()
            .reset_index()
        )

        purpose_summary.columns = ["Purpose", "Visitors"]

        for _, row in purpose_summary.iterrows():
            report.append([row["Purpose"], row["Visitors"]])

    report_df = pd.DataFrame(report)

    csv = report_df.to_csv(
        index=False,
        header=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Analysis Report",
        data=csv,
        file_name="BSP_Gate_Pass_Analysis_Report.csv",
        mime="text/csv"
    )