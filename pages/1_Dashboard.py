import streamlit as st
import pandas as pd

from utilities.python.helpers import clean_syteline_data, metrics_icon, send_email, build_filtered_dfs 

st.set_page_config(page_title="Valve Claims Dashboard", layout="wide")
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
@st.cache_data
def load_data(uploaded_file, email_list_df):
    return clean_syteline_data(uploaded_file, email_list_df)

# -------------------------------------------
today = pd.Timestamp.today().normalize()

email_list_df = pd.read_excel(r"utilities\excel\email_list.xlsx")

sheets = [
    "SyteLine Data",
    "Evaluator Count",
    "Pending Quote Approval",
    "Pending Repair",
    "Assigned for Evaluation",
    "Received"
]
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
overdue_assign_eval_df = filters["overdue_assign_eval_df"]
received_df = filters["received_df"]
pending_repair_df = filters["pending_repair_df"]
pending_quote_appr_df = filters["pending_quote_appr_df"]
pending_receipt_df = filters["pending_receipt_df"]
evaluator_count_df = filters["evaluator_count"]

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
                overdue_assign_eval_df
            ),
            "Pending Repair": (
                "To be Closed",
                pending_repair_df
            ),
            "Received": (
                "Newly Assigned",
                received_df
            ),
            "Quote Approved": (
                "Quote Approved",
                pending_quote_appr_df
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
        cur_df = evaluator_count_df
    elif selected_sheet == "Pending Quote Approval":
        cur_df = pending_quote_appr_df
    elif selected_sheet == "Pending Repair":
        cur_df = pending_repair_df
    elif selected_sheet == "Assigned for Evaluation":
        cur_df = overdue_assign_eval_df
    elif selected_sheet == "Received":
        cur_df = received_df
    
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
        text=f"Pending Rec | {len(pending_receipt_df)}", 
        font_color='#a16207',
        background_color='#fef9d7',
        border_color='#a16207',   
            )
    
# ----------------------------------------------------------------------------------------------
# ----- DATAFRAME DISPLAY FOR VARIOUS SELECTIONS -----

# ----- SyteLine Data Sheet
if selected_sheet == 'SyteLine Data':
    st.dataframe(
        filtered_syteline_df,
        width='stretch', #type: ignore
        hide_index=True,
        height=800
    )
# ----- Evaluator Count
elif selected_sheet == "Evaluator Count":
    st.dataframe(
        evaluator_count_df,
        width='stretch',  # type: ignore
        height=800
    )
    
# ----- Pending Quote Approval Sheet
elif selected_sheet == "Pending Quote Approval":
    st.dataframe(
        pending_quote_appr_df,
        width='stretch', #type: ignore
        hide_index=True,
        height=800
    )
    
# ----- Pending Repair Sheet
elif selected_sheet == "Pending Repair":
    st.dataframe(
        pending_repair_df,
        width='stretch', #type: ignore
        hide_index=True,
        height=800
    )
    
# ----- Assigned for Evaluation Sheet
elif selected_sheet == "Assigned for Evaluation":
    st.dataframe(
        overdue_assign_eval_df,
        width='stretch', #type: ignore
        hide_index=True,
        height=800
    )

# ----- Received Sheet
elif selected_sheet == "Received":
    st.dataframe(
        received_df,
        width='stretch', #type: ignore
        hide_index=True,
        height=800
    )
