# -----------------------------------------------
# Libraries
# -----------------------------------------------
import streamlit as st
from streamlit_option_menu import option_menu

from a0_SceneTreatment import *
#from pages import a1_Prospectos
from a1_CharacterDesign import *
from a2_LocationSetting import *
from a3_Admisiones import *
from a4_AyudaFinanciera import *
from a5_Inscripciones import *

#import polars as pl
import pandas as pd

# -----------------------------------------------
# Main
# -----------------------------------------------
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Lights! Prompt! Action!", page_icon=":🎬:", layout="wide")

st.sidebar.image("LPA.png", use_column_width=True)
# <a href="https://www.textstudio.com/">Font generator</a>

st.markdown(
    """
    <style> 
        section[data-testid="stSidebar"] {
            width: 400px !important; 
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------
# Sidebar
# -----------------------------------------------

with st.sidebar:
    selected = option_menu(
    menu_title = "Movie Scene Treatment", 
    options = ["Scene Treatment", "Character Design", "Environment Design", "Treatment Review", "Storyboard Design", "Preview"],
    icons = ["pencil-square", "people", "signpost-2", "bookmark-check", "pencil", "film"],
    #https://icons.getbootstrap.com
    menu_icon = "list",
    #default_index = 0, 
    #orientation = "horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#F85525"},
        "icon": {"color": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"2px", "--hover-color": "#F6DCAC"},
        "nav-link-selected": {"background-color": "#FAA968"},
    })
        
# -----------------------------------------------
# Navigation Pages
# -----------------------------------------------

if selected == "Scene Treatment":
    display_tendencias(selected)
    
if selected == "Character Design":
    display_prospectos(selected)

if selected == "Environment Design":
    display_solicitudes(selected)

if selected == "Treatment Review":
    display_admisiones(selected)

if selected == "Storyboard Design":
    display_ayudaFinanciera(selected)

if selected == "Inscripciones":
    display_inscripciones(selected)
