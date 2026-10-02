import streamlit as st
import pandas as pd

from utilities.python.general_vars_and_funcs import (global_dashboard_vars_and_data, load_data, load_raw_csv, 
                                                    build_filtered_dfs, page_config
                                                    )

from utilities.python.helpers import metrics_icon, send_email, highlight_overdue_rows 

page_config("Dashboard", "wide")
# ------------------------------------------------------------
(   today, 
    short_list_claims_df, 
    short_list_history_df, 
    email_list_df,
    lastweek_path
                                ) = global_dashboard_vars_and_data()

sheets = [
    "SyteLine Data",
    "Evaluator Count",
    "Pending Quote Approval (w/ Resp.)",
    "Pending Repair",
    "Assigned for Eval (Overdue)",
    "Received (Assigned)"
]
# ------------------------------ Main Data Upload --------------------------------
# --------------------------------------------------------------------------------
# creating location for user to upload file
uploaded_file = st.sidebar.file_uploader( "Upload SyteLine Export", type=["csv"] )

# --- if a csv file has been uploaded, save this file to session state after running cleaing function on it
# --- in addition, generate filtered dataframes for the specific claims conditions and save to session state
if uploaded_file is not None:
    raw_syteline_data_df = load_raw_csv(uploaded_file)
    syteline_data_df = load_data(uploaded_file, email_list_df)
    
    st.session_state["raw_syteline_data_df"] = raw_syteline_data_df
    st.session_state["syteline_data_df"] = syteline_data_df
    st.session_state["filters"] = build_filtered_dfs(syteline_data_df, today)

# --- if a csv file has not been uploaded, display the main page as instruction to load a file
if "syteline_data_df" not in st.session_state:
    st.warning("Please upload a SyteLine CSV export.")
    st.stop()

# --------------------------------------------------------------------------------
# loading data
syteline_data_df = st.session_state["syteline_data_df"]
current = st.session_state["filters"]

# --- reusable filters
username_notna_mask = (syteline_data_df["User Name"].notna() & (syteline_data_df["User Name"].astype(str).str.strip() != ""))

# --- Pills
selected_sheet = st.pills("Sheet", options=sheets, default=sheets[0], label_visibility="collapsed")

# creating a filtered total data dataframe that will be used for sidebar selectors
# -- this will allow for creating subsets based on combinations of:
# ------ Valve Group
# ------ Eval Status
# ------ Engineer 

filtered_syteline_df = syteline_data_df.copy()

if selected_sheet == "SyteLine Data":

    status_options = sorted(
        syteline_data_df["Evaluation Status"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    
    selected_valve_group = st.sidebar.multiselect(
    "Valve Group",
    sorted(
        syteline_data_df["Valve Group"]
        .dropna()
        .unique()
        .tolist()
        )
    )

    selected_statuses = st.sidebar.multiselect(
        "Evaluation Status",
        options=status_options,
        default=[]
    )
    
    selected_users = st.sidebar.multiselect(
    "Engineer",
    sorted(
        syteline_data_df["User Name"]
        .dropna()
        .unique()
        .tolist()
        )
    )

    if selected_valve_group:
        filtered_syteline_df = filtered_syteline_df[
            filtered_syteline_df["Valve Group"].isin(selected_valve_group)
        ]

    if selected_statuses:
        filtered_syteline_df = filtered_syteline_df[
            filtered_syteline_df["Evaluation Status"].isin(selected_statuses)
        ]

    if selected_users:
        filtered_syteline_df = filtered_syteline_df[
            filtered_syteline_df["User Name"].isin(selected_users)
        ]

# --------------------------------------------------------------------------------------------------
# creating columns for Popover tabs that will allow for user to send emails as well as display certain metrics
topcol1, topcol2, topcol3, topcol4, topcol5, topcol6 = st.columns([1, 1, 0.6, 0.7, 0.7, 0.7])

# ----- SEND MASS EMAIL BASED ON EVAL STATUS/CONDITIONS POPOVER -----
with topcol1:

    with st.popover("Send Emails", width='stretch'): #type: ignore
        us_or_cdn = st.radio("Locale1", ["Test", "US", "CDN"], horizontal=True, label_visibility='hidden')
        
        test_email = None
        
        if us_or_cdn == "Test":
            test_email = st.text_input(
                "Test Recipient",
                placeholder="last.first@smc.com",
                key="send_email_test_recip1"
            )

        selected_statuses = st.multiselect(
            "Status",
            [
                "Overdue",
                "Pending Repair",
                "Received",
                "Quote Approved"
            ]
        )

        status_map = {
            "Overdue": (
                "Overdue",
                current["overdue_assigned_eval_df"]
            ),
            "Pending Repair": (
                "To be Closed",
                current["pending_repair_df"]
            ),
            "Received": (
                "Newly Assigned",
                current["received_assigned_df"]
            ),
            "Quote Approved": (
                "Quote Approved",
                current["pending_quote_appr_res_df"]
            )
        }

        if st.button("Send", width="stretch"): #type: ignore

            for status in selected_statuses:

                email_status, df = status_map[status]

                send_email(us_or_cdn, email_status, df, test_email)

            st.success(f"Sent emails for {len(selected_statuses)} status(es)")
            
# ----------------------------------------------------------------------------------------------    
# ----- SEND INDIVIDUAL EMAIL POPOVER -----
with topcol2:
    
    with st.popover("Send Individual Email", width="stretch"):  # type: ignore
        
        us_or_cdn = st.radio("Locale2", ["Test", "US", "CDN"], horizontal=True, label_visibility='hidden')
        
        test_email = None
        
        if us_or_cdn == "Test":
            test_email = st.text_input(
                "Test Recipient",
                placeholder="last.first@smc.com",
                key="send_email_test_recip2"
            )
        
        assigned_claims_df = syteline_data_df[(username_notna_mask)]

        ccr_options = sorted(
            assigned_claims_df["CCR#"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_ccr = st.selectbox("CCR#", ccr_options)

        email_template = st.selectbox(
            "Status",
            [
                "Overdue",
                "Newly Assigned",
                "To be Closed",
                "Quote Approved",
                "Update Status"
            ]
        )

        claim_df = assigned_claims_df[assigned_claims_df["CCR#"].astype(str) == selected_ccr]

        if not claim_df.empty:

            row = claim_df.iloc[0]

            st.caption(
                f"""
                User: {row.get('User Name', '')}
                
                Status: {row.get('Evaluation Status', '')}
                
                Part: {row.get('Item', '')}
                """
            )

        if st.button("Send Individual Email", width="stretch", key="send_single_email"): #type: ignore
            send_email(us_or_cdn, email_template, claim_df, test_email)

            st.success(f"Email sent for CCR {selected_ccr}")
            
# ----------------------------------------------------------------------------------------------    
# ----- VARIOUS METRICS -----
with topcol3:
    if selected_sheet == 'SyteLine Data':
        cur_df = filtered_syteline_df
    elif selected_sheet == 'Evaluator Count':
        cur_df = current["evaluator_count"]
    elif selected_sheet == "Pending Quote Approval (w/ Resp.)":
        cur_df = current["pending_quote_appr_res_df"]
    elif selected_sheet == "Pending Repair":
        cur_df = current["pending_repair_df"]
    elif selected_sheet == "Assigned for Eval (Overdue)":
        cur_df = current["overdue_assigned_eval_df"]
    elif selected_sheet == "Received (Assigned)":
        cur_df = current["received_assigned_df"]
    
    metrics_icon(
        text=f"Current | {len(cur_df)}",
        font_color='#ff5a5f', 
        background_color='#ffeded', 
        border_color= '#ff5a5f'
    )
# ----------------------------------------------------------------------------------------------
with topcol4:
    metrics_icon(
        text = f'Total | {len(syteline_data_df)}', 
        font_color='#b45309',
        background_color='#fff4db',
        border_color='#b45309',
            )
# ----------------------------------------------------------------------------------------------
with topcol5:
    assign_rec_df = syteline_data_df[(
        (syteline_data_df['Evaluation Status'] == 'Assigned for Evaluation') |
        (syteline_data_df['Evaluation Status'] == 'Received')
    )]
    
    metrics_icon(
        text = f'Assigned/Rec | {len(assign_rec_df)}', 
        font_color='#a16207',
        background_color='#fef9d7',
        border_color='#a16207',   
            )
# ----------------------------------------------------------------------------------------------
with topcol6:
    metrics_icon(
        text=f"Pending Rec | {len(current["pending_receipt_df"])}", 
        font_color='#a16207',
        background_color='#fef9d7',
        border_color='#a16207',   
            )
    
# ----------------------------------------------------------------------------------------------
# ----- DATAFRAME DISPLAY FOR VARIOUS SELECTIONS -----

# ----- SyteLine Data Sheet
if selected_sheet == 'SyteLine Data':
    styled_df = filtered_syteline_df.sort_values('Create Date', ascending=True).style.apply(highlight_overdue_rows, axis=1)
    st.dataframe(
        styled_df,
        width='stretch',
        hide_index=True,
        height=800
    )
# ----- Evaluator Count
elif selected_sheet == "Evaluator Count":
    st.dataframe(
        current["evaluator_count"],
        width='stretch',
        height=800
    )
    
# ----- Pending Quote Approval Sheet
elif selected_sheet == "Pending Quote Approval (w/ Resp.)":
    styled_df = current["pending_quote_appr_res_df"].sort_values('Create Date', ascending=True).style.apply(highlight_overdue_rows, axis=1)
    st.dataframe(
        styled_df,
        width='stretch',
        hide_index=True,
        height=800
    )
    
# ----- Pending Repair Sheet
elif selected_sheet == "Pending Repair":
    styled_df = current["pending_repair_df"].sort_values('Create Date', ascending=True).style.apply(highlight_overdue_rows, axis=1)
    st.dataframe(
        styled_df,
        width='stretch',
        hide_index=True,
        height=800
    )
    
# ----- Assigned for Evaluation Sheet
elif selected_sheet == "Assigned for Eval (Overdue)":
    styled_df = current["overdue_assigned_eval_df"].sort_values('Create Date', ascending=True).style.apply(highlight_overdue_rows, axis=1)
    st.dataframe(
        styled_df,
        width='stretch',
        hide_index=True,
        height=800
    )

# ----- Received Sheet
elif selected_sheet == "Received (Assigned)":
    styled_df = current["received_assigned_df"].sort_values('Create Date', ascending=True).style.apply(highlight_overdue_rows, axis=1)
    st.dataframe(
        styled_df, #received_assigned_df,
        width='stretch',
        hide_index=True,
        height=800
    )
