import streamlit as st
import pandas as pd

from utilities.python.general_vars_and_funcs import load_data, page_config

from utilities.python.helpers import load_product_series_data 
# -------------------------------------------
page_config("Lists", "wide")

# -------------------------------------------
email_list_df = pd.read_excel(r"utilities\excel\updated_email_list.xlsx")
prod_series_excel_file_path = r"utilities\excel\valve_prod_series.xlsx"

prod_series_df, created_date = load_product_series_data(prod_series_excel_file_path)

filtered_email_list_df = email_list_df.copy()
filtered_prod_series_df = prod_series_df.copy()
# -------------------------------------------

selected_valve_group = st.sidebar.selectbox(
"Valve Group",
["All"] + 
sorted(
    email_list_df["Valve Group"]
    .dropna()
    .unique()
    .tolist()
    )
)

if selected_valve_group != "All":
    filtered_email_list_df = filtered_email_list_df[
        filtered_email_list_df["Valve Group"] == selected_valve_group
    ]

    filtered_prod_series_df = filtered_prod_series_df[
        filtered_prod_series_df["Product Group"] == selected_valve_group
    ]

tab1, tab2 = st.tabs(["Email List", "Product Series List"])

with tab1:
    current_email_df = st.data_editor(
                            filtered_email_list_df.sort_values('Valve Group'),
                            width='stretch',
                            height=800,
                            num_rows="dynamic"
                        )
    
    with st.sidebar:
        st.divider()
        
        update_email_list_button = st.button("Submit Email List Update", width='stretch')
        if update_email_list_button:
            if selected_valve_group != "All":
                updated_full_df = email_list_df[
                    email_list_df["Valve Group"] != selected_valve_group
                ]

                updated_full_df = pd.concat(
                    [updated_full_df, current_email_df],
                )
            else:
                updated_full_df = current_email_df


            output_file = r"utilities/excel/updated_email_list.xlsx"
            updated_full_df.to_excel(output_file, index=False, engine="openpyxl")

            st.success("Successfully updated email list")

with tab2:
        st.dataframe(
        filtered_prod_series_df,
        width='stretch',
        hide_index=True,
        height=800
    )

