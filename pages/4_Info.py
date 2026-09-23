import streamlit as st
import pandas as pd
# -------------------------------------------
st.set_page_config(
    page_title="Info",
    layout="wide"
)

# -------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 3rem;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# used for tips section
blue = "#4A90E2"

topcol1,topcol2,topcol3 = st.columns([1,3,1])
with topcol2:
        st.title("Syteline Data Export and Excel Formatting", text_alignment="center")
        st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 25px;">""",unsafe_allow_html=True)

# -------------------------------------------
f1col1, f1col2, f1col3 = st.columns([1,3,1])

# --- Image Display Column
with f1col2:
    with st.container(border=True):
        st.image(r"notes_and_information\syteline_filter_for_claims.png", width="content")

with f1col3:
    st.subheader("Step 1 - Filter Data")
    st.markdown("""Open up the <b>QC Customer Complaints</b> form in Syteline.""", unsafe_allow_html=True)
    st.markdown("""Switch from the Intake Infomration tab to the evaluation tab.
                Then, set the field Evaluation Status to <b><>Closed</b> and Evaluation Group to <b>VAL</b>""", unsafe_allow_html=True)

# -----------------------------------------------------
st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)

f2col1, f2col2, f2col3 = st.columns([1,3,1])

# --- Image Display Column
with f2col2:
    with st.container(border=True):
        st.image(r"notes_and_information\syteline_data_export.png", width="content")

with f2col1:
    st.subheader("Step 2 - Export Data")
    st.markdown("""Hover over the System tab at the top left, then hover over the Actions tab.""", unsafe_allow_html=True)
    st.markdown("""Select the <b>To Excel</b> option which will download a csv file with the data to your pc""", unsafe_allow_html=True)
    
with f2col3:
    st.markdown(f"<h3 style='color:{blue}; margin-bottom:0;'>Tips</h3>",unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""Scroll to the last row of the left sidebar for CCR numbers prior to downloading the file 
                    and right click on any index number (not the CCR number)""", unsafe_allow_html=True)
        st.markdown("""Select <b>Get more rows</b> to ensure that all claims are added because sometimes it caps at 200 initially""", unsafe_allow_html=True)

# -----------------------------------------------------
st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)

f3col1, f3col2, f3col3 = st.columns([1,3,1])

# --- Image Display Column
with f3col2:
    with st.container(border=True):
        st.image(r"notes_and_information\excel_developer_tab.png", width="content")

with f3col3:
    st.subheader("Step 3 - Developer Tab")
    st.markdown("""In the excel sheet, navigate to the <b>Developer Tab </b> at the top""", unsafe_allow_html=True)
    st.markdown("""After selecting that, select visual basic. This will open a new window""", unsafe_allow_html=True)

# -----------------------------------------------------
st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)
    
f4col1, f4col2, f4col3 = st.columns([1,3,1])

# --- Image Display Column
with f4col2:
    with st.container(border=True):
        st.image(r"notes_and_information\excel_visual_basic_window.png", width="content")

with f4col1:
    st.subheader("Step 4 - Add/Run Macro")
    st.markdown("""Now drag a copy of the claims macro (.bas file) into the left sidebar of this window.""", unsafe_allow_html=True)
    st.markdown("""After this you may, close the window. Back in the excel sheet click the <b> Macros</b> ribbon right of the previous Visual Basic one""", unsafe_allow_html=True)
    st.markdown("""Click on the macro in the new page and run it, then save the file as a .xlsm, Macro-Enabled Workbook """, unsafe_allow_html=True)
    
with f4col3:
    st.markdown(f"<h3 style='color:{blue}; margin-bottom:0;'>Tips</h3>",unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(""" If you use the web based version of Syteline, there may be a incorrectly coded value in your excel sheets last row. """, unsafe_allow_html=True)
        st.markdown(""" This will appear as mostly Japanese characters, please delete the row in excel prior to running the macro to ensure functionality. """, unsafe_allow_html=True)

# -----------------------------------------------------
st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)

f5col1, f5col2, f5col3 = st.columns([1,3,1])

# --- Image Display Column
with f5col2:
    with st.container(border=True):
        st.image(r"notes_and_information\import_data_for_dashboard.png", width="content")

with f5col3:
    st.subheader("Step 5 - Import Data")
    st.markdown("""Open up the directory in file explorer with your newly saved claims data macro enabled workbook.""", unsafe_allow_html=True)
    st.markdown("""Drag that file over into the upload section on the left sidebar of the dashboard""", unsafe_allow_html=True)

with f5col1:
    st.markdown(f"<h3 style='color:{blue}; margin-bottom:0;'>Tips</h3>",unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(""" Data can be loaded on either the <b>Overview</b> or <b>Dashboard</b> pages.""", unsafe_allow_html=True)
        st.markdown(""" This will persist until the page is manually reloaded by the user, so feel free to switch between tabs as you like. """, unsafe_allow_html=True)
        

st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 50px;">""",unsafe_allow_html=True)

f6col1, f6col2, f6col3 = st.columns([1,3,1])

with f6col2:
    st.title("Dashboard Functionality", text_alignment="center")
    st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 25px;">""",unsafe_allow_html=True)


f7col1, f7col2, f7col3 = st.columns([1,1,3])

# --- Image Display Column
with f7col3:
    with st.container(border=True):
        st.subheader("Overview Page", text_alignment="center")
        st.image(r"notes_and_information\overview_page_example.png", width="content")

with f7col1:
    with st.container(border=True):
        st.subheader("Graphs")
        st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
        
        st.markdown(""" Three graphs are displayed <br> One graph per valve group""", unsafe_allow_html=True)
        st.markdown(""" Each graph is a stacked bar chart of varying Evaluation statuses per respective valve group engineer """, unsafe_allow_html=True)
        st.markdown(""" The value listed in each graphs title within parentheses details the total number of claims active in the group """, unsafe_allow_html=True)
        
with f7col2:
    with st.container(border=True):
        st.subheader("Metrics")
        st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
        
        st.markdown(""" Various metrics have been added for quick analysis of claims distribution """, unsafe_allow_html=True)
        st.markdown(""" 
                    Metrics with a '|' divider show two values. 
                    The first value is the total number of claims with that disposition.
                    The second value details specific sub categories of the claim distribution
                    """, unsafe_allow_html=True)
        st.markdown(""" 
                    <li> <b> Disposition Received </b>: A customer response has been listed under the Non-Warranty tab in Syteline </li>
                    <li> <b> Overdue </b>: The Report Due Date, as defined by the excel macro logic, is older than the current date </li>
                    <li> <b> Assigned </b>: The claim has an engineer listed under it </li>
                    """, unsafe_allow_html=True)

st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 50px;">""",unsafe_allow_html=True)

f8col1, f8col2, f8col3 = st.columns([1,1,3])

# --- Image Display Column
with f8col3:
    with st.container(border=True):
        st.subheader("Dashboard Page", text_alignment="center")
        st.image(r"notes_and_information\dashboard_page_example.png", width="content")

with f8col1:
    with st.container(border=True):
        st.subheader("Data Selector")
        st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
        
        st.markdown(""" 
                    Located at the top of the page is a row of data selectors. 
                    Currently, <i>Syteline Data</i> is selected as indicated by the light red coloration.
                    """, unsafe_allow_html=True)
        st.markdown(""" Each page here is made as identical copy of the pages as they would be found in the macro formatted excel sheet where they come from.""", unsafe_allow_html=True)
        st.markdown(""" All other pages besides Syteline Data are static. This is indicated by the fact that no sidebar filers are displayed when they are selected. """, unsafe_allow_html=True)
        st.markdown(""" Furthermore, certain metrics populate the page to the right of the Send Email buttons. Besides, <i> Current </i>, these are static values. """, unsafe_allow_html=True)
                
with f8col2:
    with st.container(border=True):
        st.subheader("Sidebar Filter")
        st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
        
        st.markdown(""" The following sidebar filters are available when Syteline Data is selected: """, unsafe_allow_html=True)
        st.markdown(""" 
                    <li> <b> Valve Group </b> </li>
                    <li> <b> Evaluation Status </b> </li>
                    <li> <b> Engineer </b> </li>
                    """, unsafe_allow_html=True)
        
        st.markdown(""" 
                    These filters are multiselects. This means they can be selected with various combination of the unique values for the category
                    """, unsafe_allow_html=True)
        
        st.markdown(""" 
                    Moreover, these filters can be used in combination and the resulting data will update on the page. 
                    The Current metric will also update to show the total value for the selected filter(s).
                    Lastly, the columns themselves offer basic sorting by clicking directly on them.
                    """, unsafe_allow_html=True)

st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 50px;">""",unsafe_allow_html=True)

f9col1, f9col2, f9col3 = st.columns([3,1,1])

# --- Image Display Column
with f9col1:
    with st.container(border=True):
        st.subheader("Send Emails Button - Dashboard Page", text_alignment="center")
        st.image(r"notes_and_information\send_emails_example.png", width="content")

with f9col2:
    with st.container(border=True):
        st.subheader("General")
        st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
        
        st.markdown(""" 
                    The Send Emails Button is used to send mass emails based on various statuses. These statuses are:
                    """, unsafe_allow_html=True)
        st.markdown(""" 
                    <li> <b> Overdue </b>: The claim is Assigned for Evaluation and the Report Due Date has passed </li>
                    <li> <b> Pending Repair </b>: The claim is Pending Repair </li>
                    <li> <b> Received </b>: The claim is Received and an engineer has been newly assigned </li>
                    <li> <b> Quote Approved </b>: The claim is Pending Quote Approval and a customer reponse has been logged </li>
                    """, unsafe_allow_html=True)
        st.markdown(""" 
                    <br> The statuses dropdown is a multiselect so different combinations of statuses can be used and do not all have to be selected.
                    """, unsafe_allow_html=True)
        
with f9col3:
    with st.container(border=True):
        st.subheader("Specific Details")
        st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
        st.markdown(""" 
                    The default option is <b>Test</b> as indicated by the red radio button selection. 
                    This option allows the user to input a test recipient to receive the selected emails. Each email will have a subject denoted by [TEST] as well.
                    """, unsafe_allow_html=True)
        
        st.markdown(""" 
                    The US and CDN options should be selected according to the which claims are being sent. 
                    This distinction is necessary for proper function as usernames in SyteLine vary by US and CDN. 
                    If the incorrect selection is made, the username referenced may not align with the correct engineer and their respective email from the email list.
                    """, unsafe_allow_html=True)
    
        st.markdown(""" 
                    Lastly, for optimal performance, Outlook Desktop should be open on your computer even if a browser version is already. 
                    There may be a lag (~1-2 min) rarely before emails send so please do not spam if not immeadiate response. 
                    Some email batches may have small lags in the middle where the stop and then restart, please be wary of this as well.
                    """, unsafe_allow_html=True)
        

st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 50px;">""",unsafe_allow_html=True)

f10col1, f10col2, f10col3 = st.columns([1,1,3])

# --- Image Display Column
with f10col3:
    with st.container(border=True):
        st.subheader("Send Individual Emails Button - Dashboard Page", text_alignment="center")
        st.image(r"notes_and_information\send_individual_emails_example.png", width="content")

with f10col2:
    with st.container(border=True):
        st.subheader("General")
        st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
        
        st.markdown(""" 
                    The Send Individual Emails Button is used to send singular emails based on the same statuses as the mass email button
                    """, unsafe_allow_html=True)
        st.markdown(""" 
                    However, there has been one addition that uses a general purpose template calling for an update on the claims status. 
                    This can be found in the dropdown as <i> Update Status </i>
                    """, unsafe_allow_html=True)
        
with f10col1:
    with st.container(border=True):
        st.subheader("Specific Details")
        st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
        st.markdown(""" 
                    The same Test functionality as the mass send emails button exists here.
                    """, unsafe_allow_html=True)
        st.markdown(""" 
                    The only visual differences are the fields populating the botton of the button dropdown such as User, Status, and Part. 
                    These are purely to give some context as you send.
                    """, unsafe_allow_html=True)
        st.markdown(""" 
                    In addition, the list is pre filtered for only claims with engineers assigned. 
                    Therefore, you cannot send any email to a claim with no engineer already assigned to it.
                    Please wary too that while all Status options are available some may not make sense for a claim if the conditions are not accurate 
                    (setting Overdue when the claim is not technically overdue, days elapsed shown in email will not be positive)
                    """, unsafe_allow_html=True)
        