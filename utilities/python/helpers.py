import streamlit as st
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
import csv
import re
import pythoncom
import win32com.client as win32
import plotly.express as px
from openpyxl import load_workbook

# -----------------------------------------------------------------------
def load_raw_csv(file_source):

    # streamlit uploaded file
    if hasattr(file_source, "seek"):
        file_source.seek(0) # resets cursor for the file being read to the beginning

    # standard ToExcel version of syteline data from the online version
    # tries to read it as UTF-16 tab-delimited data
    try:
        return pd.read_csv(
            file_source,
            encoding="utf-16",
            sep="\t"
        )
    except Exception:
        pass

    if hasattr(file_source, "seek"):
        file_source.seek(0)

    try:
        return pd.read_csv(
            file_source,
            encoding="utf-16",
            sep="\t",
            engine="python"
        )
    except Exception:
        pass

    if hasattr(file_source, "seek"):
        file_source.seek(0)

    return pd.read_csv(
        file_source,
        encoding="utf-16",
        sep="\t",
        quoting=csv.QUOTE_NONE, # this solves an issue with the desktop saved version of syteline excel exports - parser does not treat quotes as quotes
        engine="python"
    )
# --------------------------------------------------------------------------------------------------------
def clean_syteline_data(uploaded_file, email_list_df):
    
    # --- Variables
    buis_days_till_claim_due = 10
    
    # --- loading data from csv into dataframe
    # original_data = pd.read_csv(uploaded_file, encoding="utf-16",sep="\t", engine="python")
    
    original_data = load_raw_csv(uploaded_file)

    # # addding Report Due Date, Days Since Assigned, Days Since Approved, and Days Since Quote Sent columns
    date_cols = ["Assigned Date", "Approval Date", "Quote Send Date"]

    for col in date_cols:
        original_data[col] = pd.to_datetime(original_data[col], errors="coerce")

    # --- setting Report Due Date column 
    original_data["Report Due Date"] = (original_data["Assigned Date"] + BDay(buis_days_till_claim_due)).dt.strftime("%m/%d/%Y")
    
    original_data["Report Due Date"] = pd.to_datetime(original_data["Report Due Date"],errors="coerce")

    today = np.datetime64(pd.Timestamp.today().normalize(), "D")

    # --- creating Days Since columns based off their respective intial date columns
    for source_col, new_col in [
        ("Assigned Date", "Days Since Assigned"),
        ("Approval Date", "Days Since Approved"),
        ("Quote Send Date", "Days Since Quote Sent"),
    ]:
        
        original_data[new_col] = pd.NA

        mask = original_data[source_col].notna()

        original_data.loc[mask, new_col] = np.busday_count(original_data.loc[mask, source_col].values.astype("datetime64[D]"), today) #type:ignore

    # --- not foolproof method of determining if sheet is from US or CDN syteline but works for now
    if len(str(original_data['CCR#'][0])) == 6: # CCR numbers that are US 
        og_data_with_email = pd.merge(original_data.copy(), email_list_df, left_on="User Name", right_on="userUS", how="left")
    elif len(str(original_data['CCR#'][0])) == 5: # CCR numbers that are US 
        og_data_with_email = pd.merge(original_data.copy(), email_list_df, left_on="User Name", right_on="userCDN", how="left")

    # --- setting final dataframe with similar column ordering to original excel macro
    clean_data = og_data_with_email[["Evaluation Group", "CCR#", "name", "User Name", "email", "Valve Group",
                            "Name", "Item",	"Evaluation Status", "Create Date",	
                            "Assigned Date", "Report Due Date", "Approval Date", "Quote Send Date",
                            "Quote Due Date", "Customer Response", "Evaluator's Comments ( Internal  Only)",
                            "Description", "Days Since Assigned", "Days Since Approved", "Days Since Quote Sent" ]]

    return clean_data

# --------------------------------------------------------------------------------------------------------------
# --- generates the dataframes for certain conditions from the cleaned syteline data for resuse
def build_filtered_dfs(df, today):
    
    username_notna_mask = (
        df["User Name"].notna()
        & (df["User Name"].astype(str).str.strip() != "")
    )
    
    email_notna_mask = (df["email"].notna())


    # setting up evaluator count to have unassigned index value
    pivot_df = df.copy()
    pivot_df["User Name"] = (
        pivot_df["User Name"]
        .fillna("#Unassigned")
        .replace("", "#Unassigned")
        )
        

    return {
        "assigned_eval_df": df[
            (df["Evaluation Status"] == "Assigned for Evaluation")
            & username_notna_mask
        ],

        "overdue_assigned_eval_df": df[
            (df["Evaluation Status"] == "Assigned for Evaluation")
            & username_notna_mask
            & (df["Report Due Date"] < today)
            & email_notna_mask
        ],

        "received_df": df[
            (df["Evaluation Status"] == "Received")
        ],
        
        "received_assigned_df": df[
            (df["Evaluation Status"] == "Received")
            & username_notna_mask
            & email_notna_mask
        ],

        "pending_repair_df": df[
            (df["Evaluation Status"] == "Pending Repair")
            & username_notna_mask
            & email_notna_mask
        ],
        
        "overdue_pending_repair_df": df[(df['Evaluation Status'] == "Pending Repair") 
            & (username_notna_mask)
            & (df["Report Due Date"] < today)
        ],

        "pending_quote_appr_df": df[
            (df["Evaluation Status"] == "Pending Quote Approval")
            & df["Customer Response"].notna()
            & username_notna_mask
            & email_notna_mask
        ],

        "pending_receipt_df": df[
            (df["Evaluation Status"] == "Pending Receipt")
        ],
        
        "not_from_valve_groups_df": df[
            df["Valve Group"].isna()
            & username_notna_mask
        ],
        
        "amat_df": df[
            df["Name"].str.contains(r"Applied Materials", case=False, na=False)
            & (df["Evaluation Status"] == "Pending Quote Approval") # claim is Pending Quote Approval
            & ((today - df["Quote Send Date"]).dt.days >= 14) # 45 days have elapsed since it quote was sent
            & (df["Customer Response"].isna()) # no customer response has been logged
        ],
        
        "evaluator_count": pd.pivot_table(
                    pivot_df,
                    index="User Name",
                    columns="Evaluation Status",
                    values="CCR#",
                    aggfunc="count",
                    fill_value=0,
                    margins=True,
                    margins_name="Total"
        )
    }

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
    text = text.replace("_x000D_", "\n") # Replace Excel carriage returns
    text = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags
    return text.strip()

# --------------------------------------------------------------------------------------------------------------
# Function that allows for user to end emails through their logged in instance of outlook
# --- Ideal performance with outlook desktop version already open (works well for my 2022 version, idk about different versions)
# --- Due to varied emails between US and CDN syteline, US_CDN argument must be explicitly stated to use proper emails

def send_email(US_CDN, status, claims_data, test_recipient=None):
    
    # email_list_df = pd.read_excel(r'utilities\excel\email_list.xlsx')
    
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