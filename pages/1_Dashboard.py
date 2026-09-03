import streamlit as st
import pandas as pd

from utilities.python.helpers import metrics_icon, send_email, clean_comments

# -------------------------------------------
st.set_page_config(
    page_title="Valve Claims Dashboard",
    layout="wide"
)
# -------------------------------------------
today = pd.Timestamp.today()

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
def load_workbook(file):
    return pd.read_excel(
        file,
        sheet_name=None
    )
    
# -------------------------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload Workbook",
    type=["xlsm", "xlsx"]
)

if uploaded_file:

    st.session_state["workbook"] = pd.read_excel(
        uploaded_file,
        sheet_name=None,
        engine="openpyxl",
        header=0
    )

sheets = [
    "SyteLine Data",
    "Evaluator Count",
    "Pending Quote Approval",
    "Pending Repair",
    "Assigned for Evaluation",
    "Received"
]
    
if "workbook" not in st.session_state:
    st.warning("Please upload a workbook.")
    st.stop()
    
workbook = st.session_state["workbook"] 

if workbook:
    selected_sheet = st.pills(
        "Sheet",
        options=sheets,
        default=sheets[0],
        label_visibility="collapsed"
    )
    
# ------------------------------------
# --------------- DATA ---------------
# ------------------------------------
syteline_data_df = workbook["SyteLine Data"]

# ensuring that Report Due Date column uses datetime type
syteline_data_df["Report Due Date"] = pd.to_datetime(syteline_data_df["Report Due Date"], errors="coerce")
syteline_data_df["Evaluator's Comments ( Internal  Only)"] = syteline_data_df["Evaluator's Comments ( Internal  Only)"].apply(clean_comments)

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

eval_count_df = workbook['Evaluator Count'].iloc[2:].reset_index(drop=True)
# Make first remaining row the header
eval_count_df.columns = eval_count_df.iloc[0]
# Remove the row that is now being used as headers
eval_count_df = eval_count_df.iloc[1:].reset_index(drop=True)

pending_quote_appr_df = syteline_data_df[
    (syteline_data_df["Evaluation Status"] == "Pending Quote Approval")
    & (syteline_data_df["Customer Response"].notna())
    & (syteline_data_df["User Name"].notna())
]

pending_repair_df = syteline_data_df[
    (syteline_data_df["Evaluation Status"] == "Pending Repair")
    & (syteline_data_df["User Name"].notna())
]

assign_eval_df = syteline_data_df[
    (syteline_data_df["Evaluation Status"] == "Assigned for Evaluation")
    & (syteline_data_df["User Name"].notna())
    & (syteline_data_df["Report Due Date"] < today)
]

received_df = syteline_data_df[
    (syteline_data_df["Evaluation Status"] == "Received")
    & (syteline_data_df["User Name"].notna())
    & (syteline_data_df["User Name"].astype(str).str.strip() != "")
]

# ----------------------------------------------------------------------------------------------
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
                assign_eval_df
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
        
        assigned_claims_df = syteline_data_df[
            syteline_data_df["User Name"].notna()
            & (syteline_data_df["User Name"].astype(str).str.strip() != "")
        ]

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
        cur_df = pd.DataFrame()
    elif selected_sheet == "Pending Quote Approval":
        cur_df = pending_quote_appr_df
    elif selected_sheet == "Pending Repair":
        cur_df = pending_repair_df
    elif selected_sheet == "Assigned for Evaluation":
        cur_df = assign_eval_df
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
        text = f'Pending Rec | {len(syteline_data_df[syteline_data_df['Evaluation Status'] == 'Pending Receipt'])}', 
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
        eval_count_df,
        width='stretch',  # type: ignore
        hide_index=True,
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
        assign_eval_df,
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
