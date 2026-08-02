import streamlit as st
import pandas as pd
import plotly.express as px


def show():
    st.title("🚗 Vehicle State Analysis")

    if "data" not in st.session_state:
        st.warning("Please upload an Excel file first.")
        return

    df = st.session_state["data"]

    if "vehicle_no" not in df.columns:
        st.error("vehicle_no column not found in the uploaded Excel file.")
        return

    state_codes = {
        "AP": "Andhra Pradesh",
        "AR": "Arunachal Pradesh",
        "AS": "Assam",
        "BR": "Bihar",
        "CG": "Chhattisgarh",
        "CH": "Chandigarh",
        "DL": "Delhi",
        "GA": "Goa",
        "GJ": "Gujarat",
        "HR": "Haryana",
        "HP": "Himachal Pradesh",
        "JH": "Jharkhand",
        "JK": "Jammu & Kashmir",
        "KA": "Karnataka",
        "KL": "Kerala",
        "LA": "Ladakh",
        "MH": "Maharashtra",
        "ML": "Meghalaya",
        "MN": "Manipur",
        "MP": "Madhya Pradesh",
        "MZ": "Mizoram",
        "NL": "Nagaland",
        "OD": "Odisha",
        "PB": "Punjab",
        "PY": "Puducherry",
        "RJ": "Rajasthan",
        "SK": "Sikkim",
        "TN": "Tamil Nadu",
        "TR": "Tripura",
        "TS": "Telangana",
        "UK": "Uttarakhand",
        "UP": "Uttar Pradesh",
        "WB": "West Bengal"
    }

    vehicle_numbers = (
        df["vehicle_no"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    valid_states = []
    invalid_count = 0

    for vehicle in vehicle_numbers:
        if len(vehicle) < 2:
            invalid_count += 1
            continue

        code = vehicle[:2]

        if code in state_codes:
            valid_states.append(state_codes[code])
        else:
            invalid_count += 1

    if len(valid_states) == 0:
        st.warning("No valid vehicle registration numbers found.")
        return

    state_count = (
        pd.Series(valid_states)
        .value_counts()
        .reset_index()
    )

    state_count.columns = ["State", "Vehicles"]

    total_entries = len(vehicle_numbers)
    valid_count = len(valid_states)
    total_states = len(state_count)

    top_state = state_count.iloc[0]["State"]
    top_state_count = state_count.iloc[0]["Vehicles"]

    top_percentage = round((top_state_count / valid_count) * 100, 2)

    local_count = state_count.loc[
        state_count["State"] == "Chhattisgarh",
        "Vehicles"
    ].sum()

    outside_count = valid_count - local_count

    c1, c2, c3 = st.columns(3)

    c1.metric("🚗 Total Vehicles", total_entries)
    c2.metric("✅ Valid Numbers", valid_count)
    c3.metric("⚠️ Invalid Numbers", invalid_count)

    c4, c5, c6 = st.columns(3)

    c4.metric("🗺️ States", total_states)
    c5.metric("🏆 Top State", top_state)
    c6.metric("📊 Top State %", f"{top_percentage}%")

    st.divider()

    st.subheader("📈 State-wise Vehicle Count")

    fig = px.bar(
        state_count,
        x="State",
        y="Vehicles",
        text="Vehicles",
        color="Vehicles"
    )

    fig.update_layout(
        xaxis_title="State",
        yaxis_title="Number of Vehicles"
    )

    st.plotly_chart(fig, width="stretch")

    st.divider()

    st.subheader("🥧 State Distribution")

    pie = px.pie(
        state_count,
        names="State",
        values="Vehicles"
    )

    st.plotly_chart(pie, width="stretch")

    st.divider()

    st.subheader("🚘 Local vs Outside State")

    col1, col2 = st.columns(2)

    col1.metric(
        "Local (CG)",
        local_count
    )

    col2.metric(
        "Outside State",
        outside_count
    )

    st.divider()

    st.subheader("🏅 Top 5 States")

    st.table(state_count.head(5))

    st.divider()

    st.subheader("📋 Complete State-wise Analysis")

    st.dataframe(
        state_count,
        width="stretch",
        hide_index=True
    )