import streamlit as st
import pandas as pd
import re
import pythoncom
import win32com.client as win32
import plotly.express as px
from openpyxl import load_workbook

# --------------------------------------------------------------------------------------------------------------
def metrics_icon(
        text: str, 
        background_color: str = "transparent", 
        font_color: str = "white", 
        border_color: str = '#666'
        ):
    
    st.markdown(
        f"""
        <div style="
            border: 1px solid {border_color};
            border-radius: 8px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-weight: 600;
            background-color: {background_color};
            color: {font_color};
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )
    

# ------------------------------------------------------------------------------------------------
# --------------------------------- EMAIL AUTOMATION FUNCTIONS -----------------------------------
# ------------------------------------------------------------------------------------------------  

def clean_comments(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = text.replace("_x000D_", "\n") # replace Excel carriage returns
    text = re.sub(r"<[^>]+>", "", text)  # remove HTML tags
    return text.strip()

# --------------------------------------------------------------------------------------------------------------
# Function that allows for user to end emails through their logged in instance of outlook
# --- Ideal performance with outlook desktop version already open (works well for my 2022 version, idk about different versions)
# --- Due to varied emails between US and CDN syteline, US_CDN argument must be explicitly stated to use proper emails

def send_email(US_CDN, status, claims_data, test_recipient=None):
    
    test_mode = US_CDN == "Test"
    
    if test_mode:
        claims_data = claims_data.copy()

        if "name" not in claims_data.columns:
            claims_data["name"] = "Test User"

    # # # Not necessary to merge here with merge happening prior when clean_syteline_data function is run on initial dashboard file load
    # if not test_mode:
        # Merging emails on to the claims_data dataframe
        # if US_CDN == "US":
            # claims_data = claims_data.merge(
            #     email_list_df[
            #         ["userUS", "email", "name"]
            #     ],
            #     left_on="User Name",
            #     right_on="userUS",
            #     how="left"
            # )

        # elif US_CDN == "CDN":
            # claims_data = claims_data.merge(
            #     email_list_df[
            #         ["userCDN", "email", "name"]
            #     ],
            #     left_on="User Name",
            #     right_on="userCDN",
            #     how="left"
            # )    
            
    # templates for each status
    templates = {
        # ----- Overdue Claims
        "Overdue": lambda row: f"""
            <html><body>
                <p>Hello <b>{row['name']}</b>,</p>
                <p>This is a reminder that the following claim is assigned to you.</p>
                
                <p>The claim was assigned on <b>{row['Assigned Date'].strftime('%Y-%m-%d') if pd.notna(row['Assigned Date']) else 'Not Assigned'}.</b>
                <p><span style="color:red;"> <b>{row['Days Since Assigned']}</b> days have elapsed since assignment. </span> </p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p><b>CCR:</b> {row['CCR#']}<br>
                <b>Part Number:</b> {row['Item']}<br>
                <b>Evaluation Status:</b> {row['Evaluation Status']}</p>
                <b>Evaluator Comments:</b> {row["Evaluator's Comments ( Internal  Only)"]}<br>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p>Please take the necessary actions as soon as possible.</p>
                <p><b>US-Team-UTC-ValveClaim Management Team</b></p>
                <p>Current Claims Approvers: William Stolz (Main); Martin Banghart; Joshua Eells; Saadoon Khudidah</p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
            </body></html>
        """,
        # ---- Newly assigned claims (Engineer assigned with eval status = "Received")
        "Newly Assigned": lambda row: f"""
            <html><body>
                <p>Hello <b>{row['name']}</b>,</p>
                <p>This is a notification you have been assigned a claim.</p>
                <p>Please enter Syteline and change the evaluation status from "Received" to "Assigned for Evaluation".</p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p><b>CCR:</b> {row['CCR#']}<br>
                <b>Part Number:</b> {row['Item']}<br>
                <b>Evaluation Status:</b> {row['Evaluation Status']}</p>
                <b>Evaluator Comments:</b> {row["Evaluator's Comments ( Internal  Only)"]}<br>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p>Please take the necessary actions as soon as possible.</p>
                <p><b>US-Team-UTC-ValveClaim Management Team</b></p>
                <p>Current Claims Approvers: William Stolz (Main); Martin Banghart; Joshua Eells; Saadoon Khudidah</p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
            </body></html>
        """,

        # ----- To be Closed Claims (Pending Repair)
        "To be Closed": lambda row: f"""
            <html><body>
                <p>Hello <b>{row['name']}</b>,</p>
                <p>This is a reminder you have a claim waiting to be closed.</p>
                <p><span style="color:red;"> <b>{row['Days Since Approved']}</b> days have elapsed since this claim was approved. </span> </p>
                <p>Please enter Syteline and change evaluation status to <b>Closed</b> after completing necessary rework/scrap.</p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p><b>CCR:</b> {row['CCR#']}<br>
                <b>Part Number:</b> {row['Item']}<br>
                <b>Evaluation Status:</b> {row['Evaluation Status']}</p>
                <b>Evaluator Comments:</b> {row["Evaluator's Comments ( Internal  Only)"]}<br>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p>Please take the necessary actions as soon as possible.</p>
                <p><b>US-Team-UTC-ValveClaim Management Team</b></p>
                <p>Current Claims Approvers: William Stolz (Main); Martin Banghart; Joshua Eells; Saadoon Khudidah</p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
            </body></html>
        """,
        # ----- Quote Approved Claims (Customer response has been placed on in Syteline for this claim)
        "Quote Approved": lambda row: f"""
            <html><body>
                <p>Hello <b>{row['name']}</b>,</p>
                <p>This is a reminder your claim has received an update on its pending quote.</p>
                <p> The customer response is <b>{row['Customer Response']}</b>. </p>
                
                <p> 
                Please confirm any other necessary articles to return on related email chains for customers 
                such as applied materials and complete remaining actions to close out the claim.
                </p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p><b>CCR:</b> {row['CCR#']}<br>
                <b>Part Number:</b> {row['Item']}<br>
                <b>Evaluation Status:</b> {row['Evaluation Status']}</p>
                <b>Evaluator Comments:</b> {row["Evaluator's Comments ( Internal  Only)"]}<br>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p>Please take the necessary actions as soon as possible.</p>
                <p><b>US-Team-UTC-ValveClaim Management Team</b></p>
                <p>Current Claims Approvers: William Stolz (Main); Martin Banghart; Joshua Eells; Saadoon Khudidah</p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
            </body></html>
        """,
        # Uodate Status claim (general purpose where approver can select any claim to ask update)
        "Update Status": lambda row: f"""
            <html><body>
                <p>Hello <b>{row['name']}</b>,</p>
                <p> This is a request to update the status of your claim. </p>
                <p> Please respond to this email and update the evaluators comments in Syteline accordingly</p>
                <p><span style="color:red;"> <b>{row['Days Since Assigned']}</b> days have elapsed since assignment. </span> </p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p><b>CCR:</b> {row['CCR#']}<br>
                <b>Part Number:</b> {row['Item']}<br>
                <b>Evaluation Status:</b> {row['Evaluation Status']}</p>
                <b>Evaluator Comments:</b> {row["Evaluator's Comments ( Internal  Only)"]}<br>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
                
                <p>Please take the necessary actions as soon as possible.</p>
                <p><b>US-Team-UTC-ValveClaim Management Team</b></p>
                <p>Current Claims Approvers: William Stolz (Main); Martin Banghart; Joshua Eells; Saadoon Khudidah</p>
                
                <hr style="border: 0; border-top: 1px solid #bbb; margin: 18px 0;">
            </body></html>
        """
    }

    # Email setup
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('Outlook.Application')

    successes = []
    failures = []
    
    subject_suffix = ""
    
    # map for adding label to subject 
    if status == "Overdue":
        subject_suffix = "Overdue"
    elif status == "Newly Assigned":   
        subject_suffix = "New Assignment"
    elif status == "To be Closed":
        subject_suffix = "To be Closed"
    elif status == "Quote Approved":   
        subject_suffix = "Quote Approved"
    elif status == "Update Status":   
        subject_suffix = "Update Status"

    for _, row in claims_data.iterrows():
    
        if test_mode:
            recipient = test_recipient
        else:
            recipient = row["email"]
        try:
            mail = outlook.CreateItem(0)
            mail.To = recipient
            
            if not test_mode:
                mail.CC = "US-Team-UTC-ValveClaim@1smc.onmicrosoft.com"
                
            subject_prefix = "[TEST] " if test_mode else ""
            mail.Subject = f"{subject_prefix}CCR {row['CCR#']} - {subject_suffix}"
            
            mail.HTMLBody = templates[status](row)
            mail.Send()
            # log success with details
            successes.append(f"{recipient}, CCR {row['CCR#']}, {status}")
            
        except Exception as e:
            st.error(str(e))
            raise
            
    # Summary output
    print("=== Email Send Summary ===")
    if failures:
        print("Some emails failed to send.")
        print("Successful emails:")
        for s in successes:
            print(" ", s)
        print("Failed emails:")
        for f in failures:
            recipient, ccr, stat, err = f
            print(f"{recipient}, CCR {ccr}, {stat} — Error: {err}")
    else:
        print("All emails sent successfully!")
        for s in successes:
            print(" ", s)
                
# --------------------------------------------------------------------------------------------------------------
# function to create stacked bar charts by valve group for assigned claims
# -- each bar represent an engineer
# -- each stacked part of bar represents claims assigned to them in various evaluation statuses
# -- the whole chart is filtered to one valve group (1/2/3)
def valve_group_status_chart(
    df,
    valve_group,
    title=None,
    height=375
):

    status_order = [
        "Pending Receipt",
        "Received",
        "Assigned for Evaluation",
        "Pending Quote Approval",
        "Pending Repair",
        "Closed"
    ]

    chart_df = (
        df[df["Valve Group"] == valve_group]
        .groupby(
            ["User Name", "Evaluation Status"],
            dropna=False
        )
        .size()
        .reset_index(name="Claims")
    )

    engineer_order = (
        chart_df.groupby("User Name")["Claims"]
        .sum()
        .sort_values(ascending=True)
        .index
    )

    fig = px.bar(
        chart_df,
        x="Claims",
        y="User Name",
        color="Evaluation Status",
        orientation="h",
        barmode="stack",
        title=title,
        category_orders={
            "User Name": engineer_order,
            "Evaluation Status": status_order
        }
    )

    fig.update_layout(
        height=height,
        xaxis_title="Claims",
        yaxis_title="Engineer",
        legend_title="Status",
        margin=dict(t=22, b=10, l=10, r=10)
    )

    st.plotly_chart(
        fig,
        width='content'
    )
# --------------------------------------------------------------------------------------------------------------
# function to create timeline charts by valve group for assigned claims
# -- each line represent an engineer and is populated by marks that are their claims plotted vs time
# -- the whole chart is filtered to one valve group (1/2/3)
def valve_group_timeline_chart(df, valve_group, title=None, height=375):

    sixty_days_ago = pd.Timestamp.today().normalize() - pd.Timedelta(days=60)

    chart_df = df[
        (df["Valve Group"] == valve_group)
        & (df["Assigned Date"].notna())
        & (df["User Name"].notna())
    ].copy()

    chart_df["Assigned Date"] = pd.to_datetime(
        chart_df["Assigned Date"],
        errors="coerce"
    )

    status_order = [
        "Pending Receipt",
        "Received",
        "Assigned for Evaluation",
        "Pending Quote Approval",
        "Pending Repair",
        "Closed"
    ]

    fig = px.scatter(
        chart_df,
        x="Assigned Date",
        y="User Name",
        color="Evaluation Status",
        category_orders={
            "Evaluation Status": status_order
        },
        hover_data=[
            "CCR#",
            "Name",
            "Item",
            "Evaluation Status"
        ],
        title=title
    )
    
    fig.add_vline(
        x=sixty_days_ago,
        line_color="black",
        line_width=2,
        line_dash="dash",
        annotation_text="60 Days",
        annotation_position="top"
    )

    fig.update_traces(
        marker=dict(size=10)
    )

    fig.update_layout(
        height=height,
        xaxis_title="Assigned Date",
        yaxis_title="Engineer",
        legend_title="Status",
        margin=dict(t=22, b=10, l=10, r=10)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )
    
# --------------------------------------------------------------------------
def pending_receipt_45_days_data(df):

    cutoff_date = pd.Timestamp.today().normalize() - pd.Timedelta(days=45)

    created_dates = pd.to_datetime(
        df["Create Date"],
        errors="coerce"
    )

    past_receipt_due_df = df[
        (df["Evaluation Status"] == "Pending Receipt")
        & (
            df["User Name"].isna()
            | (df["User Name"].astype(str).str.strip() == "")
        )
        & (created_dates <= cutoff_date)
    ][["CCR#", "Evaluation Status", "Name", "Create Date"]]

    return past_receipt_due_df

# --------------------------------------------------------------------------
def load_product_series_data(file_path):
    # load workbook with openpyxl and properties like created_date
    wb = load_workbook(file_path, read_only=True)
    created_date = wb.properties.created

    # read worksheet into DataFrame
    ws = wb.active
    data = pd.DataFrame(ws.values) #type:ignore

    # First row as headers
    data.columns = data.iloc[0]
    data = data.iloc[1:].reset_index(drop=True)

    # filtering down to specific columns
    select_data = data[
        [
            "Product Series",
            "Product Code [...]",
            "Product Group [...]",
            "Technical Contact [...]",
            "Secondary Technical Contact [...]",
            "Description",
        ]
    ].sort_values(by="Product Group [...]")

    # renaming columns to not have ARAS defined ellipses 
    final_data = select_data.rename(
        columns={
            "Product Code [...]": "Product Code",
            "Product Group [...]": "Product Group",
            "Technical Contact [...]": "Tech Contact",
            "Secondary Technical Contact [...]": "Secondary Tech Contact",
        }
    )
    
    # convert "UTC - Valve 1" -> 1, "UTC - Valve - 2" -> 2, etc.
    final_data["Product Group"] = (
        final_data["Product Group"]
        .astype(str)
        .str.extract(r"(\d+)$")[0]
        .astype("Int64")
    )
    
    return final_data, created_date

# --------------------------------------------------------------------

def unassigned_df_per_group(
    syteline_dataframe,
    email_dataframe,
    valve_group
):
    
    def highlight_can_assign(row):
        if row["Can_Assign"] != 0:
            return ["background-color: #fff3cd"] * len(row) # light yellow
        return [""] * len(row)

    assigned_users = set(
        syteline_dataframe["User Name"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .unique()
    )

    group_df = email_dataframe[
        email_dataframe["Valve Group"] == valve_group
    ].copy()

    assigned_mask = (
        group_df["userUS"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .isin(assigned_users)
        |
        group_df["userCDN"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .isin(assigned_users)
    )
    
    # filter for any matching User Name from overall data and userUS/userCDN from email data
    output_email_df = group_df[~assigned_mask]
    # filter out managers
    output_email_df = output_email_df[output_email_df["NOTES"] != 'Manager']
    # reorder and select specific columns
    final_df = output_email_df[['name', 'userUS', 'userCDN', 'Can_Assign', 'NOTES']]
    
    st.dataframe(final_df.style.apply(highlight_can_assign, axis=1), height=375)
    
# ---------------------------------------------------------------------------------------------
# for overview page - st.Dialog() to lookup a CCR and get a summary
# ---------------------------------------------------------------------------------------------

def dialog_info_card(title, value):
    st.markdown(
        f"""
        <div style="line-height:1.5; padding-bottom:6px;">
            <span style="color:#0082CB; font-weight:bold; font-size:0.9rem;">
                {title}
            </span><br>
            <span style="font-size:0.9rem;">
                {value}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


def dialog_text_section(title, value):
    st.markdown(
        f"""
        <div style="line-height:1.3;">
            <div style="
                color:#0082CB;
                font-weight:800;
                font-size:0.95rem;
                margin-bottom:2px;
            ">
                {title}
            </div>
            <div style="font-size:0.9rem;padding-bottom:2px;">
                {value}
        """,
            unsafe_allow_html=True,
        )

def update_card(update_num, update_status, update_date, update_notes):
    update_notes = str(update_notes).replace("\n", "<br>")

    with st.container(border=True):

        st.markdown(
            f"""
            <div style="line-height:1.15;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:0.95rem;font-weight:600;color:#0082CB;">
                        Update {update_num}
                    </span>
                    <span style="font-size:0.85rem;color:#888;">
                        {update_date:%m/%d/%Y}
                    </span>
                </div>
                <div style="
                    font-size:0.85rem;
                    color:#666;
                    margin-top:2px;
                    margin-bottom:4px;
                ">
                    {update_status}
                </div>
                <div style="
                    font-size:0.9rem;
                    line-height:1.2;
                    padding-bottom:10px
                ">
                    {update_notes}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


@st.dialog(" ", width='large', )
def lookup_claim_dialog(history_df):

    ccr = st.text_input("Enter CCR#")
    
    if ccr:
        try:
            
            cur_updates = (
                history_df[
                    history_df["CCR#"] == int(ccr)
                ]
                .sort_values("Update_Date", ascending=False)
            )
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
            
            eng_assigned = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "User Name"
            ].iloc[0]
            
            part_num = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Item"
            ].iloc[0]
            
            date_assign = st.session_state['raw_syteline_data_df'].loc[
                st.session_state['raw_syteline_data_df']["CCR#"] == int(ccr),
                "Assigned Date"
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
                subdial_col1, subdial_col2, subdial_col3 = st.columns([0.5, 0.5, 1])
                with subdial_col1:
                    with st.container(border=True):
                        dialog_info_card('Engineer', eng_assigned)
                        
                    with st.container(border=True):
                        dialog_info_card('Warranty', warranty)
                        
                with subdial_col2:
                    with st.container(border=True):
                        dialog_info_card('Part Number', part_num)
                        
                    with st.container(border=True):
                        dialog_info_card('Reason Code', reason_code)
                        
                with subdial_col3:
                    with st.container(border=True):
                        dialog_info_card('Date Assigned', date_assign)
                        
                    with st.container(border=True):
                        dialog_info_card('Customer', customer_name)
                
                with st.container(border=True):
                    dialog_text_section('Intake Information', intake_info)
                    
                    
                st.markdown("##### Claim Updates")

                for ind, (_, row) in enumerate(cur_updates.iterrows()):
                    update_card(
                        update_num=ind + 1,
                        update_status=row["Update_Status"],
                        update_date=row["Update_Date"],
                        update_notes=row["Update_Notes"],
                    )
                
            with dial_col2:
            
                with st.container(border=True):
                    dialog_text_section('Received Conditions', received_conditions)
                    st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""", unsafe_allow_html=True)
                    
                    dialog_text_section('Root Cause', root_cause)
                    st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""", unsafe_allow_html=True)
                    
                    dialog_text_section('Countermeasure', countermeasure)
                    st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""", unsafe_allow_html=True)
                    
                    dialog_text_section('Comments', eval_comments)
                    

        except (IndexError, ValueError):
            st.warning("CCR# not found")
            
# ------------------------------------------------------------------------------------------------------------            
# pandas styler function that makes dataframe row light red if current date surpasses report due date (overdue)
def highlight_overdue_rows(row):
    today = pd.Timestamp.today().normalize()
    due_date = row["Report Due Date"]

    if pd.notna(due_date) and pd.to_datetime(due_date).normalize() < today:
        return ["background-color: #ffe5e5"] * len(row)  # light red

    return [""] * len(row)