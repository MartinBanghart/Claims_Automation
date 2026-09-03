import streamlit as st
import pandas as pd
# -------------------------------------------
st.set_page_config(
    page_title="Email List",
    layout="wide"
)

# -------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 3rem;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------
email_list_df = pd.read_excel(r"utilities\excel\email_list.xlsx")

filtered_email_list_df = email_list_df.copy()


selected_valve_group = st.sidebar.multiselect(
"Valve Group",
sorted(
    email_list_df["Valve Group"]
    .dropna()
    .unique()
    .tolist()
    )
)

if selected_valve_group:
    filtered_email_list_df = filtered_email_list_df[
        filtered_email_list_df["Valve Group"].isin(selected_valve_group)
    ]   


st.dataframe(
    filtered_email_list_df,
    width='stretch', #type: ignore
    hide_index=True,
    height=800
)
