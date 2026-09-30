import streamlit as st
import pandas as pd
import numpy as np
import csv
from pathlib import Path
from pandas.tseries.offsets import BDay

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def global_dashboard_vars_and_data():
    # general
    today = pd.Timestamp.today().normalize()
    
    # files
    short_list_file = r"utilities\excel\short_list.xlsx"
    email_list_file = r"utilities\excel\updated_email_list.xlsx"
    lastweek_path = r"utilities\excel\LastWeek.csv"
    
    # file based dataframes
    short_list_claims_df = pd.read_excel(short_list_file, sheet_name="short_list_claims")
    short_list_history_df = pd.read_excel(short_list_file, sheet_name="short_list_history")
    email_list_df = pd.read_excel(email_list_file)
    
    return (
        today,
        short_list_claims_df,
        short_list_history_df,
        email_list_df,
        Path(lastweek_path)
    )
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def clean_syteline_data(uploaded_file, email_list_df, business_days_till_due):
    
    # --- Variables
    buis_days_till_claim_due = business_days_till_due
    
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
    # --> just checks length of CCR number since canada is only in 10s of thousands not 100s of thousands
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

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

# --- generates the dataframes for certain conditions from the cleaned syteline data for resuse
def build_filtered_dfs(df, today):
    
    username_notna_mask = (
        df["User Name"].notna()
        & (df["User Name"].astype(str).str.strip() != "")
    ) # mask to consolidate reused logic
    
    email_notna_mask = (df["email"].notna()) # mask to consolidate reused logic


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
            & username_notna_mask # username is not na
            & (df["Report Due Date"] < today)
            & email_notna_mask # email is not na
        ],

        "received_df": df[
            (df["Evaluation Status"] == "Received")
        ],
        
        "received_assigned_df": df[
            (df["Evaluation Status"] == "Received")
            & username_notna_mask # username is not na
            & email_notna_mask # email is not na
        ],

        "pending_repair_df": df[
            (df["Evaluation Status"] == "Pending Repair")
            & username_notna_mask # username is not na
            & email_notna_mask # email is not na
        ],
        
        "overdue_pending_repair_df": df[(df['Evaluation Status'] == "Pending Repair") 
            & (username_notna_mask)
            & (df["Report Due Date"] < today)
        ],
        
        "pending_quote_appr_df": df[
            (df["Evaluation Status"] == "Pending Quote Approval")
        ],

        "pending_quote_appr_res_df": df[
            (df["Evaluation Status"] == "Pending Quote Approval")
            & df["Customer Response"].notna()
            & username_notna_mask
            & email_notna_mask # email is not na
        ],

        "pending_receipt_df": df[
            (df["Evaluation Status"] == "Pending Receipt")
        ],
        
        "not_from_valve_groups_df": df[
            df["Valve Group"].isna() # valve group is na
            & username_notna_mask # user name is not na
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

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

@st.cache_data
def load_data(uploaded_file, email_list_df):
    return clean_syteline_data(uploaded_file, email_list_df, business_days_till_due=10)

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def page_config(title, layout):
    st.set_page_config(page_title=title, layout=layout)

    st.markdown("""
    <style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)