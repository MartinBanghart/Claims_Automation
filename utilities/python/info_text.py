import streamlit as st 
# --------------------------------------------------------------------
def image_steps_viewer(images: dict):
    """
    images = {
        "Step 1": "path1.png",
        "Step 2": "path2.png",
        "Step 3": "path3.png",
    }
    """

    tabs = st.tabs(list(images.keys()))

    for tab, image_path in zip(tabs, images.values()):
        with tab:
            st.image(image_path, width='stretch')

# --------------------------------------------------------------------

def nav_card(
    title,
    key,
    bg_color="#1E3A5F",
    text_color="white",
    height=200,
):

    st.markdown(
        f"""
        <style>
        .st-key-{key} button {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            height: {height}px !important;
            border-radius: 25px !important;

            font-weight: 600 !important;

            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            text-align: center !important;
        }}
        
        .st-key-{key} button p {{
            font-size: 2.0rem !important;
        }}

        .st-key-{key} button:hover {{
            filter: brightness(1.4);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key=key):
        return st.button(
            title,
            key=f"{key}_button",
            width='stretch',
        )
# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

def load_how_to_install():
    
    st.markdown("""
                #### To install the dashboard the key tasks to complete are:
                - [Download Python](https://www.python.org/downloads/) (Intial time only)
                - Edit environment variable **Path** for you account to include Python (Intial time only)
                - [Download VSCode](https://winget.run/pkg/Microsoft/VisualStudioCode) (Intial time only)
                - Copy over claims_automation code to secure location on your pc
                - Initialize a virtual environment within the claims_automation directory (Intial time only)
                - Run requirements.txt file in terminal to download dependencies 
                - Update batch file and create shortcut of it
                - Re-save previous approvers tracking list file to maintain history (Optional)
                
                """)
    # ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 10px; margin-bottom: 10px;">""", unsafe_allow_html=True)
    
    f1col1, f1col2, f1col3 = st.columns([1.25,3,0.8])
    
    # --- Image Display Column
    with f1col1:
        st.subheader("Step 1 - Download Python")
        st.markdown(""" Go to Python's website and click 'Download Python install manager' """, unsafe_allow_html=True)
        st.markdown(""" Follow the steps and do a standard install, It will prompt you to login as administrator, you can cancel out
                    at this point. Open a command prompt on your computer and type 'python' to continue download""", unsafe_allow_html=True)
    
    with f1col2:
        with st.container(border=True):
            image_steps_viewer({
                "python download": r"notes\how_to_install\python_download.png",
                "command prompt": r"notes\how_to_install\python_download_2.png",
            })

    with f1col3:
        st.subheader("Tips")
        st.markdown("""Verified python versions are currently 3.13.X - 3.15.X""", unsafe_allow_html=True)
        st.markdown("""""", unsafe_allow_html=True)
        
    # ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 10px; margin-bottom: 10px;">""", unsafe_allow_html=True)
    
    f2col1, f2col2, f2col3 = st.columns([1.25,3,0.8])
    
    # --- Image Display Column
    with f2col1:
        st.subheader("Step 2 - Edit Environment Variable")
        st.markdown(""" Type in **Edit Environment variable** in your pc search bar and navigate to it """, unsafe_allow_html=True)
        st.markdown(""" Select **Path** and the click **Edit** """, unsafe_allow_html=True)
        st.markdown(""" Copy and paste the file location of your Python bins directory """, unsafe_allow_html=True)
    
    with f2col2:
        with st.container(border=True):
            image_steps_viewer({
                "pc search": r"notes\how_to_install\edit_environment_variables.png",
                "select Path": r"notes\how_to_install\edit_environment_variables_2.png",
            })

    with f2col3:
        st.subheader("Tips")
        st.markdown("""""", unsafe_allow_html=True)
        st.markdown("""""", unsafe_allow_html=True)
        
# ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 10px; margin-bottom: 10px;">""", unsafe_allow_html=True)
    
    f3col1, f3col2, f3col3 = st.columns([1.25,3,0.8])
    
    # --- Image Display Column
    with f3col1:
        st.subheader("Step 3 - Download VSCode")
        st.markdown(""" Copy the following line and paste it into the command prompt """, unsafe_allow_html=True)
        st.code('winget install -e --id Microsoft.VisualStudioCode')
    
    with f3col2:
        with st.container(border=True):
            image_steps_viewer({
                "winget command": r"notes\how_to_install\download_vscode.png",
                "TBD": r"notes\how_to_install\edit_environment_variables_2.png",
            })

    with f3col3:
        st.subheader("Tips")
        st.markdown("""""", unsafe_allow_html=True)
        st.markdown("""""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 10px; margin-bottom: 10px;">""", unsafe_allow_html=True)
    
    f4col1, f4col2, f4col3 = st.columns([1.25,3,0.8])
    
    # --- Image Display Column
    with f4col1:
        st.subheader("Step 4 - Saving the Code")
        st.markdown(""" A copy of the code files can be found in the US-Team-UTC-ValveClaim Teams channel.
                    It will specifically be within the general chat with a directory called **Automation**. """, unsafe_allow_html=True)
        st.markdown(""" It is recommended to save it in a file location directly on your pc and not within the OneDrive.
                        This can be navigated to within the file explorer via This PC > Windows (C:) > Users > USERNAME > Documents """, unsafe_allow_html=True)
    
    with f4col2:
        with st.container(border=True):
            image_steps_viewer({
                "Where to find the files": r"notes\how_to_install\code_location.png",
                "Where to save": r"notes\how_to_install\save_location_for_code.png",
            })

    with f4col3:
        st.subheader("Tips")
        st.markdown("""""", unsafe_allow_html=True)
        st.markdown("""""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 10px; margin-bottom: 10px;">""", unsafe_allow_html=True)
    
    f5col1, f5col2, f5col3 = st.columns([1.25,3,0.8])
    
    # --- Image Display Column
    with f5col1:
        st.subheader("Step 5 - Creating Virtual Environment")
        st.markdown(""" To create a shortcut, the batch file, LaunchDashboard, located in the utilities directory will
                        need to be updated. Right click the file and select 'Edit in Notepad' """, unsafe_allow_html=True)
        st.markdown(""" Only one change needs to be made on the second line. Within the parentheses, replace the placeholder
                        with the actual location of the directory for your claims_automation code""", unsafe_allow_html=True)
        st.markdown(""" After saving the batch file, right click it in the file explorer and create a shortcut.
                        Then, drag it on to your desktop. You can use this to open it.""", unsafe_allow_html=True)
    
    with f5col2:
        with st.container(border=True):
            image_steps_viewer({
                "Batch File Location": r"notes\how_to_install\batch_file_location.png",
                "Batch File": r"notes\how_to_install\batch_file.png",
            })

    with f5col3:
        st.subheader("Tips")
        st.markdown(""" After the intial creation of your virtual environment, you may need to restart VSCode""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 10px; margin-bottom: 10px;">""", unsafe_allow_html=True)
    
    f6col1, f6col2, f6col3 = st.columns([1.25,3,0.8])
    
    # --- Image Display Column
    with f6col1:
        st.subheader("Step 6 - Creating a Shortcut")
        st.markdown(""" To create a shortcut, the batch file, LaunchDashboard, located in the utilities directory will
                        need to be updated. Right click the file and select 'Edit in Notepad' """, unsafe_allow_html=True)
        st.markdown(""" Only one change needs to be made on the second line. Within the parentheses, replace the placeholder
                        with the actual location of the directory for your claims_automation code""", unsafe_allow_html=True)
        st.markdown(""" After saving the batch file, right click it in the file explorer and create a shortcut.
                        Then, drag it on to your desktop. You can use this to open it.""", unsafe_allow_html=True)
    
    with f6col2:
        with st.container(border=True):
            image_steps_viewer({
                "Batch File Location": r"notes\how_to_install\batch_file_location.png",
                "Batch File": r"notes\how_to_install\batch_file.png",
            })

    with f6col3:
        st.subheader("Tips")
        st.markdown(""" Whenever you use your shortcut to open the dashboard, 
                        it will generate a terminal window as well as a browser page with your dashboard.
                        The dashboard requires the terminal window to stay active while in use, otherwise it will not work.
                        When you are done with your dashboard, simply close your browser page and click on your terminal.
                        By clicking **Ctrl+C**, the program will be stopped and prompt you to enter **Y** to terminate it completely. """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

def load_data_information():

    # used for tips section
    blue = "#4A90E2"

    f1col1, f1col2, f1col3 = st.columns([1,3,1])
    
    # --- Image Display Column
    with f1col2:
        with st.container(border=True):
            st.image(r"notes\syteline_filter_for_claims.png", width="content")

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
            st.image(r"notes\syteline_data_export.png", width="content")

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
            st.markdown(""" If you use the web based version of Syteline, there may be a incorrectly coded value in your excel sheets last row. """, unsafe_allow_html=True)
            st.markdown(""" This will appear as mostly Japanese characters, please delete the row in excel prior to running the macro to ensure functionality. """, unsafe_allow_html=True)

    # -----------------------------------------------------
    st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)

    f3col1, f3col2, f3col3 = st.columns([1,3,1])

    with f3col1:
        st.markdown(f"<h3 style='color:{blue}; margin-bottom:0;'>Tips</h3>",unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(""" Data can be loaded on either the <b>Overview</b>, <b>Dashboard</b>, and or <b>Tracking</b> pages.""", unsafe_allow_html=True)
            st.markdown(""" This will persist until the page is manually reloaded by the user, so feel free to switch between tabs as you like. """, unsafe_allow_html=True)
            
    # --- Image Display Column
    with f3col2:
        with st.container(border=True):
            st.image(r"notes\import_data_for_dashboard.png", width="content")

    with f3col3:
        st.subheader("Step 3 - Import Data")
        st.markdown("""Open up the directory in file explorer with your newly saved claims data macro enabled workbook.""", unsafe_allow_html=True)
        st.markdown("""Drag that file over into the upload section on the left sidebar of the dashboard""", unsafe_allow_html=True)
            
# ----------------------------------------------------------------------------            
# ----------------------------------------------------------------------------   
# ---------------------------------------------------------------------------- 

def load_overview_page_information():
    sm_cont_height = 500
    med_cont_height = 650
    lg_cont_height = 850
    f1col1, f1col2, f1col3 = st.columns([1,1,3])

    # Slide 1 - General Overview
    with f1col1:
        with st.container(border=True, height=sm_cont_height):
            st.subheader("Graphs")
            st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
            
            st.markdown(""" Three graphs are displayed. <br> One graph per valve group""", unsafe_allow_html=True)
            st.markdown(""" Each graph is a stacked bar chart of varying Evaluation statuses per respective valve group engineer """, unsafe_allow_html=True)
            st.markdown(""" The value listed in each graphs title within parentheses details the total number of claims active in the group """, unsafe_allow_html=True)
            st.markdown(""" Via the radio selector above each graph, a timeline graph and a data sheet of 
                        engineers not assigned claims can be displayed """, unsafe_allow_html=True)

    with f1col2:
        with st.container(border=True, height=sm_cont_height):
            st.subheader("Metrics")
            st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
            
            st.markdown(""" Various metrics have also been added for quick analysis of claims distribution. 
                        These can be seen in the bottom right corner of the page""", unsafe_allow_html=True)
            st.markdown(""" 
                        This section can also displayed varied data through the radio selector above it. The default is **Stats**
                        which gives a general comparison between the currently loaded sheet and the sheet loaded as LastWeek
                        """, unsafe_allow_html=True)

    with f1col3:
        with st.container(border=True, height=sm_cont_height):
            st.image(r'notes\overview_page\overview_page_example.png')
    
    # ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)
        
    f2col1, f2col2 = st.columns([1.5,3])

    # Slide 2 - Graphs
    with f2col1:
        with st.container(border=True, height=med_cont_height):
            st.subheader("Graphs")
            st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
            
            st.markdown(""" The Bar and Timeline graph options display claims across all evaluation statuses so long as an engineer has been assigned""", unsafe_allow_html=True)
            st.markdown(""" By clicking on a status in the legend, it can be removed and the graph updated to focus on specific statuses.
                            By double clicking a status, all statuses except for that one will be removed.""", unsafe_allow_html=True)
            st.markdown(""" In the timeline graph, by hovering over a data point, specific information related to the claim is displayed. """, unsafe_allow_html=True)
            st.markdown(""" The Unassigned data sheet gives a list of who is not assigned any claims. 
                        Currently, it will highlight in <span style="color:#B8860B"> yellow </span> any engineer who has a **Can_Assign** 
                        value that is not 0 (scale of 0-10) to indicate they are not prohibited to be assigned claims. 
                        The scale is approver/manager controlled and is a general reference for percentage (ex. 5 = 50% workload; 0 = 0% workload).""", unsafe_allow_html=True)
    
    # --- Image Display Column
    with f2col2:
        with st.container(border=True, height=med_cont_height):
            image_steps_viewer({
                "Bar": r"notes\overview_page\overview_graph_1.png",
                "Timeline": r"notes\overview_page\overview_graph_2.png",
                "Unassigned": r"notes\overview_page\overview_graph_3.png",
            })
            
    # ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)
        
    f3col1, f3col2 = st.columns([1.5,3])

    # Slide 3 - Metrics
    with f3col1:
        with st.container(border=True, height=lg_cont_height):
            st.subheader("Metrics")
            st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
            
            st.markdown(""" The first page shows stats for different important evaluation statuses and conditions. 
                        Below each stat is a delta value to indicate the change as compared to the loaded LastWeek data.
                        The color indicates if the trend is positive or negative based on the specific metric""", unsafe_allow_html=True)
            
            st.markdown("""
            The metrics are defined as follows:

            <ul>
                <li><b>Pending Receipt</b>: All claims pending receipt</li>
                <li><b>Assigned for Eval</b>: All claims assigned for evaluation; subset for those overdue (report due date older than current date) </li>
                <li><b>Pending Quote</b>: All claims pending quote; subset for those with a confirmed customer response</li>
                <li><b>Received</b>: All claims received; subset for those with engineers assigned (need to switch to assigned for themselves)</li>
                <li><b>Pending Repair</b>: All claims pending repair; subset for those overdue (report due date older than current date)</li>
            </ul>
            """, unsafe_allow_html=True)
            st.markdown("""
            The other pages show varied subsets of data:

            <ul>
                <li><b>Pend. Rcpt. (+45 d)</b>: All assigned claims pending receipt with a create date older than 45 days</li>
                <li><b>AMAT No Resp. (+45 d)</b>: All assigned claims from AMAT with no quote response and a quote send date older than 45 days</li>
                <li><b>Non-AMAT Quote (+30 d)</b>: All assigned claims, not from AMAT, with a quote response date older than 30 days</li>
                <li><b>Non-Valve</b>: All valve claims assigned to a user that is not listed as being a part of any valve group</li>
            </ul>
            """, unsafe_allow_html=True)

    
    # --- Image Display Column
    with f3col2:
        with st.container(border=True, height=lg_cont_height):
            image_steps_viewer({
                "Stats": r"notes\overview_page\overview_metrics_1.png",
                "Pending Receipt(+45 d)": r"notes\overview_page\overview_metrics_2.png",
                "AMAT No Resp(+45 d)": r"notes\overview_page\overview_metrics_3.png",
                "Non-AMAT Quote(+30 d)": r"notes\overview_page\overview_metrics_4.png",
                "Non-Valve": r"notes\overview_page\overview_metrics_5.png",
            })

    # ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)
        
    f4col1, f4col2 = st.columns([1,3])

    # Slide 4 - Lookup CCR
    with f4col1:
        with st.container(border=True, height=med_cont_height+50):
            st.subheader("Lookup CCR")
            st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
            
            st.markdown(""" The lookup CCR functionality is intended to give a quick summary of a claim in question""", unsafe_allow_html=True)
            st.markdown(""" After clicking the button, a popup will appear to enter the CCR number""", unsafe_allow_html=True)
            st.markdown(""" After hitting enter, it will show a summary of the claim in question detailing things such as
                            the assigned engineer, part number, customer, assigned date, the report so far as written, and etc""", unsafe_allow_html=True)
            st.markdown(""" Moreover, it shows updates that have been created in the tracking page under the respective claim""", unsafe_allow_html=True)

    # --- Image Display Column
    with f4col2:
        with st.container(border=True, height=med_cont_height+50):
            image_steps_viewer({
                "lookup CCR button": r"notes\overview_page\overview_lookup_ccr_1.png",
                "lookup Report": r"notes\overview_page\overview_lookup_ccr_2.png",
            })
    # ---------------------------------------------------------------------
    st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 45px;">""",unsafe_allow_html=True)
        
    f5col1, f5col2 = st.columns([1,3])

    # Slide 4 - Lookup CCR
    with f5col1:
        with st.container(border=True, height=med_cont_height+50):
            st.subheader("Update LastWeek Data")
            st.markdown("""<hr style="height: 1px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""",unsafe_allow_html=True)
            
            st.markdown(""" The Update LastWeek Data functionality is intended to simplify the process of loading a previous weeks data""", unsafe_allow_html=True)
            st.markdown(""" After clicking the button, a popup will appear to upload a csv export from syteline""", unsafe_allow_html=True)
            st.markdown(""" Typically, a csv file used during wednesdays meeting is used. Once the file is uploaded and the user clicks save.
                        The pages metrics will update to reflect this change. It will also persist into future sessions.""", unsafe_allow_html=True)
            st.markdown(""" There is also no need to change name the file a specific name. So long as the file is a typical csv export from Syteline it should work.
                        Please be wary if using the online version of syteline to delete the last row with japanese characters to avoid issue.""", unsafe_allow_html=True)

    # --- Image Display Column
    with f5col2:
        with st.container(border=True, height=med_cont_height+50):
            image_steps_viewer({
                "update lastweek button": r"notes\overview_page\overview_update_lastweek_1.png",
                "data upload popup": r"notes\overview_page\overview_update_lastweek_2.png",
            })
            
    st.markdown(" ") # blank space at bottom for aesthetic
# ----------------------------------------------------------------------------            
# ----------------------------------------------------------------------------   
# ----------------------------------------------------------------------------  

def load_dashboard_page_information():
    f1col1, f1col2, f1col3 = st.columns([1,1,3])

    # --- Image Display Column
    with f1col3:
        with st.container(border=True):
            st.subheader("Dashboard Page", text_alignment="center")
            st.image(r"notes\dashboard_page_example.png", width="content")

    with f1col1:
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
                    
    with f1col2:
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
            
    # -----------------------------------------------
    st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 50px;">""",unsafe_allow_html=True)

    f2col1, f2col2, f2col3 = st.columns([3,1,1])

    # --- Image Display Column
    with f2col1:
        with st.container(border=True):
            st.subheader("Send Emails Button - Dashboard Page", text_alignment="center")
            st.image(r"notes\send_emails_example.png", width="content")

    with f2col2:
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
            
    with f2col3:
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
            
    # -----------------------------------------------------
    st.markdown("""<hr style="height: 3px;border: none; background-color: #666; margin-top: 35px; margin-bottom: 50px;">""",unsafe_allow_html=True)

    f3col1, f3col2, f3col3 = st.columns([1,1,3])

    # --- Image Display Column
    with f3col3:
        with st.container(border=True):
            st.subheader("Send Individual Emails Button - Dashboard Page", text_alignment="center")
            st.image(r"notes\send_individual_emails_example.png", width="content")

    with f3col2:
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
            
    with f3col1:
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