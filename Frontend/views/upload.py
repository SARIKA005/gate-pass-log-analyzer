import streamlit as st
import pandas as pd


def show_upload():

    st.title("📂 Upload Gate Pass Log")

    # If data is already loaded
    if "data" in st.session_state:

        st.success("✅ Excel file already uploaded.")

        if st.button("🔄 Upload Another File"):
            del st.session_state["data"]
            st.rerun()

        df = st.session_state["data"]

        st.subheader("Preview")
        st.dataframe(
            df,
            width="stretch"
        )

        # Gate-wise Bar Chart
        if "Gate No" in df.columns:
            st.subheader("🚪 Gate-wise Visitor Analysis")

            gate_count = df["Gate No"].value_counts()

            st.bar_chart(gate_count)

        return


    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=["xlsx"]
    )


    if uploaded_file is not None:

        try:

            df = pd.read_excel(uploaded_file)

            # Remove completely empty rows
            df = df.dropna(how="all")

            # Remove leading/trailing spaces from column names
            df.columns = df.columns.str.strip()

            # Remove the instruction/note row at the bottom (if present)
            first_column = df.columns[0]

            df = df[
                ~df[first_column]
                .astype(str)
                .str.strip()
                .str.lower()
                .str.startswith("note")
            ]
            # Reset row numbers after removing rows
            df = df.reset_index(drop=True)

            st.session_state["data"] = df
            st.write("Total Rows Loaded:", len(df))
            st.success("✅ File uploaded successfully!")

            st.subheader("Preview")

            st.dataframe(
                df,
                width="stretch"
            )


            # Gate-wise Bar Chart
            if "Gate No" in df.columns:

                st.subheader("🚪 Gate-wise Visitor Analysis")

                gate_count = df["Gate No"].value_counts()

                st.bar_chart(gate_count)


        except Exception as e:

            st.error(f"Error reading file: {e}")