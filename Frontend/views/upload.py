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
            use_container_width=True
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
            df = df.astype(str)   
            st.session_state["data"] = df

            st.success("✅ File uploaded successfully!")

            st.subheader("Preview")

            st.dataframe(
                df,
                use_container_width=True
            )


            # Gate-wise Bar Chart
            if "Gate No" in df.columns:

                st.subheader("🚪 Gate-wise Visitor Analysis")

                gate_count = df["Gate No"].value_counts()

                st.bar_chart(gate_count)


        except Exception as e:

            st.error(f"Error reading file: {e}")