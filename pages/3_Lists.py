import streamlit as st
import pandas as pd

from utilities.python.helpers import load_product_series_data 
# -------------------------------------------
st.set_page_config(page_title="Lists", layout="wide")

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
prod_series_excel_file_path = r"utilities\excel\valve_prod_series.xlsx"
prod_series_df, created_date = load_product_series_data(prod_series_excel_file_path)

filtered_email_list_df = email_list_df.copy()
filtered_prod_series_df = prod_series_df.copy()
# -------------------------------------------

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
    
    filtered_prod_series_df = filtered_prod_series_df[
        filtered_prod_series_df["Product Group"].isin(selected_valve_group)
    ] 

tab1, tab2 = st.tabs(["Email List", "Product Series List"])

with tab1:
    st.dataframe(
        filtered_email_list_df,
        width='stretch',
        hide_index=True,
        height=800
    )

with tab2:
        st.dataframe(
        filtered_prod_series_df,
        width='stretch',
        hide_index=True,
        height=800
    )
