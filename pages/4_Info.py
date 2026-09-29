import streamlit as st
import pandas as pd

from utilities.python.info_text import summary_information, load_data_information, maintenance_information
# -------------------------------------------
st.set_page_config(page_title="Info", layout="wide")

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
# -------------------------------------------

with st.sidebar:
    topic = st.selectbox("Topic",
            ("Summary", "How-To", "Maintenance", "Claims"),
            index=0
            )

# creating lists of subpages for a given topic to feed to st.pills()
if topic == "Summary":
    subpages = []
elif topic == "How-To":
    subpages = ["Load Data", "Send Emails"]
elif topic == "Maintenance":
    subpages = ["Manual Files"]
elif topic == "Claims":
    subpages = ["Approver Routine", "Applied Materials"]
    
# -------------------------------------------
# subpage display at the top of page
subpage_selected = st.pills("subpages", subpages, label_visibility='hidden')

# if len(subpages) > 0:
#     st.markdown("""<hr style="height: 2px;border: none; background-color: #666; margin-top: 0px; margin-bottom: 20px;">""",unsafe_allow_html=True)

# calling info_text functions to display text on page for given topic and subpage
if topic == "Summary":
    summary_information()
    
elif topic == "How-To":
    if subpage_selected == "Load Data":
        load_data_information()
        
elif topic == "Maintenance":
    maintenance_information()
    
elif topic == "Claims":
    st.markdown('Claims Selected')