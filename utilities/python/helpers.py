import streamlit as st
import pandas as pd
import re

import pythoncom
import win32com.client as win32

import plotly.express as px

# ------------------------------------------------
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

# Function that allows for user to end emails through their logged in instance of outlook
# --- Ideal performance with outlook desktop version already open (works well for my 2022 version, idk about different versions)
# --- Due to varied emails between US and CDN syteline, US_CDN argument must be explicitly stated to use proper emails

def send_email(US_CDN, status, claims_data, test_recipient=None):
    
    email_list_df = pd.read_excel(r'utilities\excel\email_list.xlsx')
    
    test_mode = US_CDN == "Test"
    
    if test_mode:
        claims_data = claims_data.copy()

        if "name" not in claims_data.columns:
            claims_data["name"] = "Test User"

    if not test_mode:
        # Merging emails on to the claims_data dataframe
        if US_CDN == "US":
            claims_data = claims_data.merge(
                email_list_df[
                    ["userUS", "email", "name"]
                ],
                left_on="User Name",
                right_on="userUS",
                how="left"
            )

        elif US_CDN == "CDN":
            claims_data = claims_data.merge(
                email_list_df[
                    ["userCDN", "email", "name"]
                ],
                left_on="User Name",
                right_on="userCDN",
                how="left"
            )    
    
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
                <p><span style="color:red;"> <b>{row['Days Since Assigned']}</b> days have elapsed since this claim was approved. </span> </p>
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
                
# ------------------------------------------------------------------------------------------------

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
        legend_title="Status"
    )

    st.plotly_chart(
        fig,
        width='content'
    )