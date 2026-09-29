import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from utilities.python.helpers import (  valve_group_status_chart, valve_group_timeline_chart, load_raw_csv,
                                        clean_syteline_data, build_filtered_dfs, pending_receipt_45_days_data,
                                        unassigned_df_per_group )

st.set_page_config(page_title="Overview", layout="wide")
# ------------------------------------------------------------
today = pd.Timestamp.today().normalize()

email_list_df = pd.read_excel(r"utilities\excel\updated_email_list.xlsx")
# ------------------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 3rem;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)
# -------------------------------------------
@st.cache_data
def load_data(uploaded_file, email_list_df):
    return clean_syteline_data(uploaded_file, email_list_df)

# ------------------------------------------------------------
# load last week's snapshot if it exists
lastweek_path = Path(r"utilities\excel\LastWeek.csv")

if lastweek_path.exists():
    lw_data_df = load_data(lastweek_path, email_list_df)
    
    st.session_state["lw_filters"] = build_filtered_dfs(lw_data_df, today)
    lw_filters = st.session_state["lw_filters"]

    lw_assigned_eval_df = lw_filters["assigned_eval_df"]
    lw_overdue_assigned_eval_df = lw_filters["overdue_assigned_eval_df"]
    lw_received_df = lw_filters["received_df"]
    lw_received_assigned_df = lw_filters["received_assigned_df"]
    lw_pending_repair_df = lw_filters["pending_repair_df"]
    lw_overdue_pending_repair_df = lw_filters["overdue_pending_repair_df"]
    lw_pending_quote_appr_res_df = lw_filters["pending_quote_appr_df"]
    lw_pending_receipt_df = lw_filters["pending_receipt_df"]
    lw_evaluator_count_df = lw_filters["evaluator_count"]
else:
    st.session_state["lastweek_df"] = None

# ------------------------------------------------------------
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
filters = st.session_state["filters"]

assigned_eval_df = filters["assigned_eval_df"]
overdue_assigned_eval_df = filters["overdue_assigned_eval_df"]
received_df = filters["received_df"]
received_assigned_df = filters["received_assigned_df"]
pending_repair_df = filters["pending_repair_df"]
overdue_pending_repair_df = filters["overdue_pending_repair_df"]
pending_quote_appr_res_df = filters["pending_quote_appr_df"]
pending_receipt_df = filters["pending_receipt_df"]
evaluator_count_df = filters["evaluator_count"]
not_from_valve_groups_df = filters["not_from_valve_groups_df"]
amat_df = filters["amat_df"]

# --- reusable filters
username_notna_mask = (syteline_data_df["User Name"].notna() & (syteline_data_df["User Name"].astype(str).str.strip() != ""))
# ------------------------------------------------------------

@st.dialog("Lookup CCR", width='large', )
def lookup_claim_dialog():

    ccr = st.text_input("Enter CCR#")

    if ccr:
        try:
            # ------------------
            
            non_warranty_status = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Non-Warranty Repair"
            ].iloc[0]
            
            if non_warranty_status == 0:
                warranty = 'Yes'
            elif non_warranty_status == 1:
                warranty = 'No'
                
                
            reason_code = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Reason Code"
            ].iloc[0]
            
            customer_name = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Name"
            ].iloc[0]
            
            intake_info = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Description"
            ].iloc[0]
            
            received_conditions = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Received Conditions (Appearance and Performance)"
            ].iloc[0]
            
            root_cause = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Root Cause"
            ].iloc[0]
            
            countermeasure = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Countermeasure"
            ].iloc[0]
            
            eval_comments = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Evaluator's Comments ( Internal  Only)"
            ].iloc[0]
            # ------------------
            
            dial_col1, dial_col2 = st.columns([1,1])
            
            with dial_col1:
                subdial_col1, subdial_col2, subdial_col3 = st.columns([0.4, 0.4, 1])
                with subdial_col1:
                    with st.container(border=True):
                        st.markdown(f"##### Warranty")
                        st.markdown(f"###### **{warranty}**")
                        
                with subdial_col2:
                    with st.container(border=True):
                        st.markdown(f"##### Reason Code")
                        st.markdown(f"###### **{reason_code}**")
                        
                with subdial_col3:
                    with st.container(border=True):
                        st.markdown(f"##### Customer")
                        st.markdown(f"###### **{customer_name}**")
                
                with st.container(border=True):
                    st.markdown("### Intake Information")
                    st.write(intake_info)
                
            with dial_col2:
            
                with st.container(border=True):
                    st.markdown("### Received Conditions")
                    st.write(received_conditions)
                    st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 5px;">""", unsafe_allow_html=True)
                    
                    st.markdown("### Root Cause")
                    st.write(root_cause)
                    st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 5px;">""", unsafe_allow_html=True)
                    
                    st.markdown("### Countermeasure")
                    st.write(countermeasure)
                    st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 5px;">""", unsafe_allow_html=True)
                    
                    st.markdown("### Comments")
                    st.write(eval_comments)

        except (IndexError, ValueError):
            st.warning("CCR# not found")
            
with st.sidebar:
    if st.button("Lookup CCR", width='stretch'):
        lookup_claim_dialog()

# ------------------------------------------------------------
# # ----- SyteLine Data Sheet
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
        stats_radio = st.radio(label ="stats_radio", options = ["General Stats", "45 Days Pending", "Outsiders", "AMAT"], 
                                horizontal=True, index=0, label_visibility="collapsed")
        
        subcol1, subcol2 = st.columns([1,1])
        
        if stats_radio == "General Stats":
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
                                value=f"{len(assigned_eval_df)} ",
                                delta=f"{len(assigned_eval_df)-len(lw_assigned_eval_df)}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                        
                    with metric_col2:
                        st.metric(
                                label="Overdue", 
                                value=f"{len(overdue_assigned_eval_df)}",
                                delta=f"{len(overdue_assigned_eval_df)-len(lw_overdue_assigned_eval_df)}",
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
                                value=f"{len(received_df)}",
                                delta=f"{len(received_df)-len(lw_received_df)}",
                                delta_color="inverse",
                                delta_description="since last week"
                                )
                        
                    with metric_col2:
                        st.metric(
                                label="Assigned", 
                                value=f"{len(received_assigned_df)}",
                                delta=f"{len(received_assigned_df)-len(lw_received_assigned_df)}",
                                delta_color="inverse",
                                delta_description="since last week"
                                )
                    
            with subcol2:
                # --------------------------------------------------------------------
                with st.container(border=True): # ----- PENDING RECEIPT METRICS
                    st.metric(
                            label="Pending Receipt", 
                            value=f"{len(pending_receipt_df)}",
                            delta=f"{len(pending_receipt_df)-len(lw_pending_receipt_df)}",
                            delta_color="inverse",
                            delta_description="since last week"
                            )
                    
                with st.container(border=True): # ----- PENDING QUOTE APPROVAL METRICS
                    pending_quote_appr = len(syteline_data_df[syteline_data_df['Evaluation Status'] == "Pending Quote Approval"])
                    lw_pending_quote_appr = len(lw_data_df[lw_data_df['Evaluation Status'] == "Pending Quote Approval"])
                    
                    metric_title_col1, metric_title_col2, metric_title_col3 = st.columns([0.5, 1, 0.3])
                    with metric_title_col2:
                        st.markdown("<h6>Pending Quote</h6>",unsafe_allow_html=True)
                    
                    metric_col1, metric_col2 = st.columns([1,1])
                    with metric_col1:
                        st.metric(
                                label="Total", 
                                value=f"{pending_quote_appr}",
                                delta=f"{(pending_quote_appr)-(lw_pending_quote_appr)}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                    
                    with metric_col2:
                        st.metric(
                                label="Disposition Received", 
                                value=f"{len(pending_quote_appr_res_df)}",
                                delta=f"{len(pending_quote_appr_res_df)-len(lw_pending_quote_appr_res_df)}",
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
                                value=f"{len(pending_repair_df)}",
                                delta=f"{len(pending_repair_df)-len(lw_pending_repair_df)}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                    with metric_col2:
                        st.metric(
                                label="Overdue", 
                                value=f"{len(overdue_pending_repair_df)}",
                                delta=f"{len(overdue_pending_repair_df)-len(lw_overdue_pending_repair_df)}",
                                delta_color="inverse",
                                delta_description="last week"
                                )
                    
        elif stats_radio == "45 Days Pending":
            st.dataframe(pending_receipt_45_days_data(st.session_state["syteline_data_df"]), height=350)
            
        elif stats_radio == "Outsiders":
            st.dataframe(not_from_valve_groups_df, height=350)
            
        elif stats_radio == "AMAT":
            st.dataframe(amat_df, height=350)
            
            
