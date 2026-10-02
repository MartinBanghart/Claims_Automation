import streamlit as st 
from pathlib import Path


LAST_WEEK_DIR = Path(r"utilities\excel")

@st.dialog(" ", width="large")
def update_last_week_dialog():

    uploaded_file = st.file_uploader(
        "Upload Last Week CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        st.success(
            f"Selected file: {uploaded_file.name}"
        )

        if st.button(
            "Save as LastWeek.csv",
            type="primary",
            width="stretch"
        ):

            save_path = LAST_WEEK_DIR / "LastWeek.csv"

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success("LastWeek.csv updated successfully!")
            st.cache_data.clear()
            st.rerun()