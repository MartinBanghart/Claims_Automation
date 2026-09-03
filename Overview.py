import streamlit as st
import pandas as pd

import plotly.express as px

from utilities.python.helpers import valve_group_status_chart

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

# ------------------------------------------------------------
today = pd.Timestamp.today()

# ------------------------------------------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload Workbook",
    type=["xlsm", "xlsx"]
)

if uploaded_file is not None:
    st.session_state["workbook"] = pd.read_excel(
        uploaded_file,
        sheet_name=None,
        engine="openpyxl",
        header=0
    )

if "workbook" not in st.session_state:
    st.warning("Please upload a workbook.")
    st.stop()

workbook = st.session_state["workbook"]
# ------------------------------------------------------------

# # ----- SyteLine Data Sheet
syteline_data_df = workbook["SyteLine Data"]

def group_subset(group_num):
    return syteline_data_df[
        (syteline_data_df['Valve Group'] == group_num)
        & (syteline_data_df["User Name"].notna())
        ]

col1, col2 = st.columns([1,1])

with col1:
    with st.container(border=True):
        valve_group_status_chart(syteline_data_df, 1, title=f"Valve Group 1 ({len(group_subset(1))})")
    with st.container(border=True):
        valve_group_status_chart(syteline_data_df, 3, title=f"Valve Group 3 ({len(group_subset(3))})")
        
with col2:
    with st.container(border=True):
        valve_group_status_chart(syteline_data_df, 2, title=f"Valve Group 2 ({len(group_subset(2))})")
        
    subcol1, subcol2 = st.columns([1,1])
    
    with subcol1:
        with st.container(border=True): # ----- TOTAL METRIC
            st.metric(label="Total", value=len(syteline_data_df))
            
        with st.container(border=True):# ----- ASSIGNED FOR EVAL METRICS
            assigned = len(syteline_data_df[(syteline_data_df["Evaluation Status"] == "Assigned for Evaluation") & (syteline_data_df["User Name"].notna())])
            overdue_assign_eval = len(syteline_data_df[(syteline_data_df['Evaluation Status'] == "Assigned for Evaluation") 
                & (syteline_data_df["User Name"].notna())
                & (syteline_data_df["Report Due Date"] < today)]
            )
            st.metric(label="Assigned for Evaluation | Overdue", value=f"{assigned} | {overdue_assign_eval}")
            
        with st.container(border=True): # ----- RECEIVED METRICS
            rec = len(syteline_data_df[syteline_data_df['Evaluation Status'] == "Received"])
            rec_assigned = len(syteline_data_df[(syteline_data_df['Evaluation Status'] == "Received") & (syteline_data_df["User Name"].notna())])
            st.metric(label="Received | Assigned", value=f"{rec} | {rec_assigned}")
            
    with subcol2:
        with st.container(border=True): # ----- PENDING QUOTE APPROVAL METRICS
            pending_quote_appr = len(syteline_data_df[syteline_data_df['Evaluation Status'] == "Pending Quote Approval"])
            pending_quote_appr_rec = len(syteline_data_df[(syteline_data_df['Evaluation Status'] == "Pending Quote Approval") & (syteline_data_df["Customer Response"].notna())])
            st.metric(label="Pending Quote | Disposition Received", value=f"{pending_quote_appr} | {pending_quote_appr_rec}")
            
        with st.container(border=True): # ----- PENDING REPAIR METRICS
            pending_repair = len(syteline_data_df[(syteline_data_df['Evaluation Status'] == "Pending Repair") & (syteline_data_df["User Name"].notna())])
            overdue_pending_repair = len(syteline_data_df[(syteline_data_df['Evaluation Status'] == "Pending Repair") 
                        & (syteline_data_df["User Name"].notna())
                        & (syteline_data_df["Report Due Date"] < today)]
                        )
            st.metric(label="Pending Repair | Overdue ", value=f"{pending_repair} | {overdue_pending_repair}")
            
        with st.container(border=True): # ----- PENDING RECEIPT METRICS
            pending_receipt = len(syteline_data_df[(syteline_data_df['Evaluation Status'] == "Pending Receipt")])
            st.metric(label="Pending Receipt", value=f"{pending_receipt}")