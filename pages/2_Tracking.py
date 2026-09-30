import streamlit as st
import pandas as pd
import math

from utilities.python.global_vars_and_funcs import (global_dashboard_vars_and_data, load_data, load_raw_csv, 
                                                    build_filtered_dfs, page_config
                                                    )

page_config('Tracking', 'wide')
# -------------------------------------------
def display_claim_card(cur_claim, short_list_df, short_list_history_df):

    claim_row = short_list_df.loc[short_list_df["CCR#"] == cur_claim].iloc[0]

    cur_eng = claim_row["Assigned_Engineer"]
    cur_assign_date = claim_row["Assigned_Date"]

    days_open = (pd.Timestamp.today().normalize() - cur_assign_date).days

    cur_updates = (
        short_list_history_df[
            short_list_history_df["CCR#"] == cur_claim
        ]
        .sort_values("Update_Date", ascending=False)
    )

    with st.container(border=True):

        header_col1, header_col2, header_col3 = st.columns([1, 2, 1])

        with header_col2:
            st.markdown(
                f"""
                <div style="font-size:1.25rem;font-weight:600;margin-bottom:2px;">
                    CCR {cur_claim}
                </div>
                """,
                unsafe_allow_html=True,
            )

        subheader_col1, subheader_col2, subheader_col3 = st.columns(3)

        with subheader_col1:
            st.markdown(f"**Engineer**  \n{cur_eng}")

        with subheader_col2:
            st.markdown(f"**Assigned**  \n{cur_assign_date:%m/%d/%Y}")

        with subheader_col3:
            st.markdown(f"**Days Open**  \n{days_open}")

        st.markdown('<hr style="margin:0.1rem 0;">', unsafe_allow_html=True)

        for ind, (_, row) in enumerate(cur_updates.iterrows()):

            with st.container(border=True):

                h1, h2 = st.columns([2, 1])

                with h1:
                    st.markdown(f"**Update {ind+1}**")
                    st.caption(row["Update_Status"])

                with h2:
                    st.markdown(row["Update_Date"].strftime("%m/%d/%Y"))

                st.write(row["Update_Notes"])

# -------------------------------------------------------------------------------------
today = pd.Timestamp.today().normalize()

email_list_df = pd.read_excel(r"utilities\excel\email_list.xlsx")

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

not_pending_rec = syteline_data_df[
    (syteline_data_df["Evaluation Status"] != "Pending Receipt") &
    (syteline_data_df["User Name"].notna())
]

short_list_file = r"utilities\excel\short_list.xlsx"
short_list_claims_df = pd.read_excel(short_list_file, sheet_name="short_list_claims")
short_list_history_df = pd.read_excel(short_list_file, sheet_name="short_list_history")


active_claims = set(syteline_data_df["CCR#"].dropna())
claims = short_list_claims_df[short_list_claims_df["CCR#"].isin(active_claims)]["CCR#"].tolist()

cards_per_page = 3
num_pages = max(1, math.ceil(len(claims) / cards_per_page))


# --------------------------------------------------------------------------------

if num_pages > 1:
    page = st.radio(
        "Page",
        options=list(range(1, num_pages + 1)),
        horizontal=True,
        label_visibility='hidden'
    )
else:
    page = 1
    
start_idx = (page - 1) * cards_per_page
end_idx = start_idx + cards_per_page

page_claims = claims[start_idx:end_idx]

mcol1, mcol2, mcol3, mcol4 = st.columns([1,1,1,1])
claim_cols = [mcol1, mcol2, mcol3]

for i, claim in enumerate(page_claims):
    with claim_cols[i]:
        display_claim_card(
            claim,
            short_list_claims_df,
            short_list_history_df
        )

with mcol4:
    with st.container(border=True):
        scol4_L, scol4_M, scol4_R = st.columns([0.7,1,0.5])
        # start of form to add an update to the list
        with scol4_M:
            st.subheader("Update")
        # setting the ccr to be updated outside of form to allow for refresh of values displayed at bottom above submit
        active_ccr = not_pending_rec['CCR#'].astype(int).unique().tolist()
        ccr_to_update = st.selectbox('Enter CCR Number', options=active_ccr)
        if ccr_to_update:
            current = syteline_data_df[syteline_data_df["CCR#"]==ccr_to_update]
            assigned_eng = current["User Name"].iloc[0]
            eval_status = current["Evaluation Status"].iloc[0]
            eval_comments = current["Evaluator's Comments ( Internal  Only)"].iloc[0]
            assigned_date = current["Assigned Date"].iloc[0]
            
        with st.form("add_update", border=False):
            date_of_update = st.date_input('Enter Date')
            update_notes = st.text_area('Enter Notes')
            
            st.divider()
            # basic info for selected CCR
            if ccr_to_update:
                st.markdown(f'**Assigned Engineer:** {assigned_eng}')
                st.markdown(f'**Evaluation Status:** {eval_status}')
                st.write(f'**Evaluators Comments:** {eval_comments}')
            
            submitted = st.form_submit_button("submit", width='stretch')
            
            if submitted:

                # Reload workbook
                claims_df = pd.read_excel(short_list_file, sheet_name="short_list_claims")
                history_df = pd.read_excel(short_list_file, sheet_name="short_list_history")

                # ----------------------------------------------------
                # Add claim if not already on short list

                if ccr_to_update not in claims_df["CCR#"].values:

                    new_claim = pd.DataFrame({
                        "CCR#": [ccr_to_update],
                        "Assigned_Engineer": [assigned_eng],
                        "Assigned_Date": [assigned_date]
                    })

                    claims_df = pd.concat([claims_df, new_claim], ignore_index=True)

                # ----------------------------------------------------
                # add history entry

                new_history = pd.DataFrame({
                    "CCR#": [ccr_to_update],
                    "Update_Date": [date_of_update],
                    "Update_Status": [eval_status],
                    "Update_Notes": [update_notes]
                })

                history_df = pd.concat([history_df, new_history], ignore_index=True)

                # ----------------------------------------------------
                # save workbook

                with pd.ExcelWriter(short_list_file, engine="openpyxl", mode="w") as writer:

                    claims_df.to_excel(writer, sheet_name="short_list_claims", index=False)
                    
                    history_df.to_excel(writer, sheet_name="short_list_history", index=False)

                st.success(f"Update saved for CCR {ccr_to_update}")
                st.rerun()



