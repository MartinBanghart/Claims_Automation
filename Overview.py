import streamlit as st
import pandas as pd
import plotly.express as px

from utilities.python.general_vars_and_funcs import (global_dashboard_vars_and_data, load_data, load_raw_csv, 
                                                    build_filtered_dfs, page_config
                                                    )

from utilities.python.overview_helpers import update_last_week_dialog

from utilities.python.helpers import (  valve_group_status_chart, valve_group_timeline_chart,
                                        pending_receipt_45_days_data, unassigned_df_per_group, lookup_claim_dialog
                                        )

page_config("Overview", "wide")
# ------------------------------------------------------------
(   today, 
    short_list_claims_df, 
    short_list_history_df, 
    email_list_df,
    lastweek_path
                            ) = global_dashboard_vars_and_data()

# ------------------------------ Main Data Upload --------------------------------
# creating location for user to upload file
uploaded_file = st.sidebar.file_uploader( "Upload SyteLine Export", type=["csv"])

# --- if a csv file has been uploaded, save this file to session state after running a cleaning function on it
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

# ------------------------------------------------------------
# --- loading last weeks data
if lastweek_path.exists():
    lw_data_df = load_data(lastweek_path, email_list_df)
    
    st.session_state["lw_filters"] = build_filtered_dfs(lw_data_df, today)
    lw = st.session_state["lw_filters"]
    
else:
    st.session_state["lastweek_df"] = None

# --------------------------------------------------------------------------------
# --- loading current data
syteline_data_df = st.session_state["syteline_data_df"]
current = st.session_state["filters"]

# --- reusable filters
username_notna_mask = (syteline_data_df["User Name"].notna() & (syteline_data_df["User Name"].astype(str).str.strip() != ""))

# ------------------------------------------------------------
# --- dialog pop up that allows for viewing summary of selected claim
with st.sidebar:
    st.divider()
    
    if st.button("Lookup CCR", width='stretch'):
        lookup_claim_dialog(short_list_history_df)
        
    st.divider()
    
    if st.button("Update LastWeek Data", width='stretch'):
        update_last_week_dialog()

# ------------------------------------------------------------
# # ----- function that creates filter for a specific valve group; simplifies graph loading functions
def group_subset(group_num):
    return syteline_data_df[
        (syteline_data_df['Valve Group'] == group_num)
        & (syteline_data_df["User Name"].notna())
        ]

# ---------------------------------------------------------------------------------------------------
# ------------------------------------------- PAGE LAYOUT -------------------------------------------
# ---------------------------------------------------------------------------------------------------

col1, col2 = st.columns([1,1])

with col1:
    with st.container(border=True):
        choice_vg1_graph = st.radio(label ="radio_graph1", options = ["Bar", "Timeline", "Unassigned"], key="vg1_radio",
                                    horizontal=True, index=0, label_visibility="collapsed")
        if choice_vg1_graph == "Bar":
            valve_group_status_chart(syteline_data_df, 1, title=f"Valve Group 1 ({len(group_subset(1))})")
        elif choice_vg1_graph == "Timeline":
            valve_group_timeline_chart(syteline_data_df, 1, title=f"Valve Group 1 Timeline ({len(group_subset(1))})")
        elif choice_vg1_graph == "Unassigned":
            unassigned_df_per_group(syteline_data_df, email_list_df, 1)
            
    with st.container(border=True):
        choice_vg3_graph = st.radio(label ="radio_graph3", options = ["Bar", "Timeline", "Unassigned"], key="vg3_radio",
                                    horizontal=True, index=0, label_visibility="collapsed")
        if choice_vg3_graph == "Bar":
            valve_group_status_chart(syteline_data_df, 3, title=f"Valve Group 3 ({len(group_subset(3))})")
        elif choice_vg3_graph == "Timeline":
            valve_group_timeline_chart(syteline_data_df, 3, title=f"Valve Group 3 Timeline ({len(group_subset(3))})")
        elif choice_vg3_graph == "Unassigned":
            unassigned_df_per_group(syteline_data_df, email_list_df, 3)

with col2:
    with st.container(border=True):
        choice_vg2_graph = st.radio(label ="radio_graph2", options = ["Bar", "Timeline", "Unassigned"], key="vg2_radio",
                                    horizontal=True, index=0, label_visibility="collapsed")
        if choice_vg2_graph == "Bar":
            valve_group_status_chart(syteline_data_df, 2, title=f"Valve Group 2 ({len(group_subset(2))})")
        elif choice_vg2_graph == "Timeline":
            valve_group_timeline_chart(syteline_data_df, 2, title=f"Valve Group 2 Timeline ({len(group_subset(2))})")
        elif choice_vg2_graph == "Unassigned":
            unassigned_df_per_group(syteline_data_df, email_list_df, 2)
    
    with st.container(border=True):  
        stats_radio = st.radio(label ="stats_radio", 
                                options = ["Stats", "Pend. Rcpt.(+45 d)", "AMAT No Resp.(+45 d)", "Non-AMAT Quote(+30 d)", "Non-Valve"], 
                                horizontal=True, index=0, label_visibility="collapsed")
        
        subcol1, subcol2 = st.columns([1,1])
        
        if stats_radio == "Stats":
            with subcol1:
                with st.container(border=True): # ----- TOTAL METRIC
                    st.metric(
                            label="Total", 
                            value=len(syteline_data_df), 
                            delta=len(syteline_data_df)-len(lw_data_df), 
                            delta_color="inverse",
                            delta_description="since last week"
                            )
                # ------------------------------------------------------     
                with st.container(border=True): # ----- ASSIGNED FOR EVAL METRICS
                    metric_title_col1, metric_title_col2, metric_title_col3 = st.columns([0.4, 1, 0.10])
                    with metric_title_col2:
                        st.markdown("<h6>Assigned for Eval</h6>",unsafe_allow_html=True)
                    
                    metric_col1, metric_col2 = st.columns([1,1])
                    with metric_col1:
                        st.metric(
                                label="Total", 
                                value=f"{len(current["assigned_eval_df"])} ",
                                delta=f"{len(current["assigned_eval_df"])-len(lw["assigned_eval_df"])}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                        
                    with metric_col2:
                        st.metric(
                                label="Overdue", 
                                value=f"{len(current["overdue_assigned_eval_df"])}",
                                delta=f"{len(current["overdue_assigned_eval_df"])-len(lw["overdue_assigned_eval_df"])}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                # ------------------------------------------------------    
                with st.container(border=True): # ----- RECEIVED METRICS
                    metric_title_col1, metric_title_col2, metric_title_col3 = st.columns([0.75, 1, 0.3])
                    with metric_title_col2:
                        st.markdown("<h6>Received</h6>",unsafe_allow_html=True)
                    
                    metric_col1, metric_col2 = st.columns([1,1])
                    with metric_col1:
                        st.metric(
                                label="Total", 
                                value=f"{len(current["received_df"])}",
                                delta=f"{len(current["received_df"])-len(lw["received_df"])}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                        
                    with metric_col2:
                        st.metric(
                                label="Assigned", 
                                value=f"{len(current["received_assigned_df"])}",
                                delta=f"{len(current["received_assigned_df"])-len(lw["received_assigned_df"])}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                    
            with subcol2:
                # --------------------------------------------------------------------
                with st.container(border=True): # ----- PENDING RECEIPT METRICS
                    st.metric(
                            label="Pending Receipt", 
                            value=f"{len(current["pending_receipt_df"])}",
                            delta=f"{len(current["pending_receipt_df"])-len(lw["pending_receipt_df"])}",
                            delta_color="inverse",
                            delta_description="since last week"
                            )
                    
                with st.container(border=True): # ----- PENDING QUOTE APPROVAL METRICS
                    metric_title_col1, metric_title_col2, metric_title_col3 = st.columns([0.5, 1, 0.3])
                    with metric_title_col2:
                        st.markdown("<h6>Pending Quote</h6>",unsafe_allow_html=True)
                    
                    metric_col1, metric_col2 = st.columns([1,1])
                    with metric_col1:
                        st.metric(
                                label="Total", 
                                value=f"{len(current['pending_quote_appr_df'])}",
                                delta=f"{(len(current['pending_quote_appr_df']))-(len(lw['pending_quote_appr_df']))}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                    
                    with metric_col2:
                        st.metric(
                                label="Disposition Received", 
                                value=f"{len(current["pending_quote_appr_res_df"])}",
                                delta=f"{len(current["pending_quote_appr_res_df"])-len(lw["pending_quote_appr_res_df"])}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                    
                with st.container(border=True): # ----- PENDING REPAIR METRICS
                    metric_title_col1, metric_title_col2, metric_title_col3 = st.columns([0.5, 1, 0.25])
                    with metric_title_col2:
                        st.markdown("<h6>Pending Repair</h6>",unsafe_allow_html=True)
                        
                    metric_col1, metric_col2 = st.columns([1,1])
                    with metric_col1:
                        st.metric(
                                label="Total", 
                                value=f"{len(current["pending_repair_df"])}",
                                delta=f"{len(current["pending_repair_df"])-len(lw["pending_repair_df"])}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                    with metric_col2:
                        st.metric(
                                label="Overdue", 
                                value=f"{len(current["overdue_pending_repair_df"])}",
                                delta=f"{len(current["overdue_pending_repair_df"])-len(lw["overdue_pending_repair_df"])}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                    
        elif stats_radio == "Pend. Rcpt.(+45 d)":
            st.dataframe(pending_receipt_45_days_data(st.session_state["syteline_data_df"]), height=350)    
            
        elif stats_radio == "AMAT No Resp.(+45 d)":
            st.dataframe(current["amat_df"], height=350)
            
        elif stats_radio == "Non-AMAT Quote(+30 d)":
            st.dataframe(current["non_amat_quote_30_day_plus"], height=350)
            
        elif stats_radio == "Non-Valve":
            st.dataframe(current["not_from_valve_groups_df"], height=350)
            
            
