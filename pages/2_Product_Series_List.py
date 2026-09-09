import streamlit as st
import pandas as pd

from utilities.python.helpers import clean_syteline_data, build_filtered_dfs, load_product_series_data 

st.set_page_config(page_title="Prod Series List", layout="wide")
# ----------------------------------------------------------

today = pd.Timestamp.today().normalize()

email_list_df = pd.read_excel(r"utilities\excel\email_list.xlsx")

prod_series_excel_file_path = r"utilities\excel\valve_prod_series.xlsx"
final_data, created_date = load_product_series_data(prod_series_excel_file_path)

# ----------------------------------------------------------
@st.cache_data
def load_data(uploaded_file, email_list_df):
    return clean_syteline_data(uploaded_file, email_list_df)

# ------------------------------ Main Data Upload --------------------------------

# creating location for user to upload file
uploaded_file = st.sidebar.file_uploader( "Upload SyteLine Export", type=["csv"] )

# --- if a csv file has been uploaded, save this file to session state after running cleaing function on it
# --- in addition, generate filtered dataframes for the specific claims conditions and save to session state
if uploaded_file is not None:
    syteline_data_df = load_data(uploaded_file, email_list_df)
    
    st.session_state["syteline_data_df"] = syteline_data_df
    st.session_state["filters"] = build_filtered_dfs(syteline_data_df, today)

# --- if a csv file has not been uploaded, display the main page as instruction to load a file
if "syteline_data_df" not in st.session_state:
    st.warning("Please upload a SyteLine CSV export.")
    st.stop()

# --------------------------------------------------------------------------
mcol1, mcol2 = st.columns([2,0.25])

with mcol1:
    st.write(f"Date Created: {created_date:%m/%d/%Y %H:%M}" if created_date else "No created date found")
    st.dataframe(final_data, width='stretch', height=800, hide_index=True)

# with mcol2:
#     st.write("Claims by Product Code")