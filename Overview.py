import streamlit as st
import pandas as pd
import plotly.express as px

from utilities.python.helpers import (  valve_group_status_chart, valve_group_timeline_chart, load_raw_csv,
                                        clean_syteline_data, build_filtered_dfs, pending_receipt_45_days_data)

st.set_page_config(page_title="Overview", layout="wide")
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
today = pd.Timestamp.today().normalize()

email_list_df = pd.read_excel(r"utilities\excel\email_list.xlsx")
# ------------------------------------------------------------
# ------------------------------ Main Data Upload --------------------------------
# --------------------------------------------------------------------------------
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

# --- reusable filters
username_notna_mask = (syteline_data_df["User Name"].notna() & (syteline_data_df["User Name"].astype(str).str.strip() != ""))
# ------------------------------------------------------------

eval_comment_lookup = st.sidebar.text_input("Enter CCR# to See Comments")

if eval_comment_lookup:
    try:
        comments = syteline_data_df.loc[
            syteline_data_df["CCR#"] == int(eval_comment_lookup),
            "Evaluator's Comments ( Internal  Only)"
        ].iloc[0]

        st.sidebar.markdown(comments)
    except (IndexError, ValueError):
        st.sidebar.warning("CCR# not found")
        

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
        choice_vg1_graph = st.radio(label ="radio_graph1", options = ["Bar", "Timeline"], horizontal=True, index=0, label_visibility="collapsed")
        if choice_vg1_graph == "Bar":
            valve_group_status_chart(syteline_data_df, 1, title=f"Valve Group 1 ({len(group_subset(1))})")
        elif choice_vg1_graph == "Timeline":
            valve_group_timeline_chart(syteline_data_df, 1, title=f"Valve Group 1 Timeline ({len(group_subset(1))})")
            
    with st.container(border=True):
        choice_vg3_graph = st.radio(label ="radio_graph3", options = ["Bar", "Timeline"], horizontal=True, index=0, label_visibility="collapsed")
        if choice_vg3_graph == "Bar":
            valve_group_status_chart(syteline_data_df, 3, title=f"Valve Group 3 ({len(group_subset(3))})")
        elif choice_vg3_graph == "Timeline":
            valve_group_timeline_chart(syteline_data_df, 3, title=f"Valve Group 3 Timeline ({len(group_subset(3))})")

with col2:
    with st.container(border=True):
        choice_vg2_graph = st.radio(label ="radio_graph2", options = ["Bar", "Timeline"], horizontal=True, index=0, label_visibility="collapsed")
        if choice_vg2_graph == "Bar":
            valve_group_status_chart(syteline_data_df, 2, title=f"Valve Group 2 ({len(group_subset(2))})")
        elif choice_vg2_graph == "Timeline":
            valve_group_timeline_chart(syteline_data_df, 2, title=f"Valve Group 2 Timeline ({len(group_subset(2))})")
    
    with st.container(border=True):  
        stats_radio = st.radio(label ="stats_radio", options = ["General Stats", "45 Days Pending", "Outsiders"], horizontal=True, index=0, label_visibility="collapsed")
        
        subcol1, subcol2 = st.columns([1,1])
        
        if stats_radio == "General Stats":
            with subcol1:
                with st.container(border=True): # ----- TOTAL METRIC
                    st.metric(label="Total", value=len(syteline_data_df))
                    
                with st.container(border=True): # ----- ASSIGNED FOR EVAL METRICS
                    st.metric(label="Assigned for Evaluation | Overdue", value=f"{len(assigned_eval_df)} | {len(overdue_assigned_eval_df)}")
                    
                with st.container(border=True): # ----- RECEIVED METRICS
                    st.metric(label="Received | Assigned", value=f"{len(received_df)} | {len(received_assigned_df)}")
                    
            with subcol2:
                with st.container(border=True): # ----- PENDING QUOTE APPROVAL METRICS
                    pending_quote_appr = len(syteline_data_df[syteline_data_df['Evaluation Status'] == "Pending Quote Approval"])
                    st.metric(label="Pending Quote | Disposition Received", value=f"{pending_quote_appr} | {len(pending_quote_appr_res_df)}")
                    
                with st.container(border=True): # ----- PENDING REPAIR METRICS
                    st.metric(label="Pending Repair | Overdue ", value=f"{len(pending_repair_df)} | {len(overdue_pending_repair_df)}")
                    
                with st.container(border=True): # ----- PENDING RECEIPT METRICS
                    pending_receipt = len(syteline_data_df[(syteline_data_df['Evaluation Status'] == "Pending Receipt")])
                    st.metric(label="Pending Receipt", value=f"{pending_receipt}")
            
        elif stats_radio == "45 Days Pending":
            st.dataframe(pending_receipt_45_days_data(st.session_state["syteline_data_df"]), height=350)
            
        elif stats_radio == "Outsiders":
            st.dataframe(not_from_valve_groups_df, height=350)
            
            
