# -----------------------------------------------
# Libraries
# -----------------------------------------------
import streamlit as st
from streamlit_option_menu import option_menu

#from pages import a0_Tendencias
from a0_Tendencias import *
#from pages import a1_Prospectos
from a1_Promocion import *
from a2_Solicitudes import *
from a3_Admisiones import *
from a4_AyudaFinanciera import *
from a5_Inscripciones import *

import polars as pl
import pandas as pd

# -----------------------------------------------
# Main
# -----------------------------------------------
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="CRM Insights (Info Sapiens + Ibero)", page_icon=":clapper_board:", layout="wide")

st.sidebar.image("ibero_logo-nobg.png", use_column_width=True)

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
    menu_title = "Proceso de Registro", 
    options = ["Tendencias históricas", "Promoción", "Solicitudes", "Admisiones", "Ayuda Financiera", "Inscripciones"],
    icons = ["clock-history", "megaphone", "pencil-square", "person-check-fill", "cash-coin", "book"],
    menu_icon = "list",
    #default_index = 0, 
    #orientation = "horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#E3B025"},
        "icon": {"color": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"2px", "--hover-color": "#af1839"},
        "nav-link-selected": {"background-color": "#660c18"},
    })
        
# -----------------------------------------------
# Navigation Pages
# -----------------------------------------------

if selected == "Tendencias históricas":
    display_tendencias(selected)
    
if selected == "Promoción":
    display_prospectos(selected)

if selected == "Solicitudes":
    display_solicitudes(selected)

if selected == "Admisiones":
    display_admisiones(selected)

if selected == "Ayuda Financiera":
    display_ayudaFinanciera(selected)

if selected == "Inscripciones":
    display_inscripciones(selected)
