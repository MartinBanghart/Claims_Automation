import streamlit as st
import pandas as pd

from utilities.python.general_vars_and_funcs import (global_dashboard_vars_and_data, page_config)
from utilities.python.info_text import (nav_card, load_data_information, load_overview_page_information,
                                        load_dashboard_page_information, load_how_to_install
                                        )

# -------------------------------------------
page_config("Info", "wide")

# -------------------------------------------
with st.sidebar:
    home = st.button('Home', width='stretch')
    if home:
        st.session_state.selected_page = None
        
# -------------------------------------------

if "selected_page" not in st.session_state:
    st.session_state.selected_page = None

if st.session_state.selected_page is None:
    
    mcol1, mcol2, mcol3 = st.columns([1,1,1])
    base_card_height = 160
    
    with mcol1:
            if nav_card('How to Install Dashboard', 'nav_card1',
                    bg_color="#048243",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "install"
            
            if nav_card('Loading Data into Dashboard', 'nav_card2',
                    bg_color="#048243",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "load_data"
                
            if nav_card('Content 3', 'nav_card3',
                    bg_color="#048243",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "content_3"
                
            if nav_card('Content 4', 'nav_card4',
                    bg_color="#048243",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "content_4"
            
    with mcol2:
            if nav_card('Overview Page Summary', 'nav_card5',
                    bg_color="#1E3A5F",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "overview_summary"
                
            if nav_card('Dashboard Page Summary', 'nav_card6',
                    bg_color="#1E3A5F",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "dashboard_summary"
                
            if nav_card('Tracking Page Summary', 'nav_card7',
                    bg_color="#1E3A5F",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "tracking_summary"
                
            if nav_card('List Page Summary', 'nav_card8',
                    bg_color="#1E3A5F",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "list_summary"
                
    with mcol3:
            if nav_card('Content 9', 'nav_card9',
                    bg_color="#592A9C",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "content_9"
                
            if nav_card('Content 10', 'nav_card10',
                    bg_color="#592A9C",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "content_10"
                
            if nav_card('Content 11', 'nav_card11',
                    bg_color="#592A9C",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "content_11"
                
            if nav_card('Content 12', 'nav_card12',
                    bg_color="#592A9C",
                    text_color="white",
                    height=base_card_height,
                ):
                st.session_state.selected_page = "content_12"
else:
    
    if st.session_state.selected_page == "install":
        st.header('Install Page')
        st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""", unsafe_allow_html=True)
        load_how_to_install()

    elif st.session_state.selected_page == "load_data":
        st.header('Loading Data Page')
        st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""", unsafe_allow_html=True)
        load_data_information()

    elif st.session_state.selected_page == "overview_summary":
        st.header('Overview Page')
        st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""", unsafe_allow_html=True)
        load_overview_page_information()

    elif st.session_state.selected_page == "dashboard_summary":
        st.header('Dashboard Page')
        st.markdown("""<hr style="height: 2px; border: none; background-color: #666; margin-top: 0px; margin-bottom: 0px;">""", unsafe_allow_html=True)
        load_dashboard_page_information()