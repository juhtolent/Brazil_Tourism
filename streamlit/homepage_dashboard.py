import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from st_pages import Page, Section, add_page_title, show_pages


st.set_page_config(page_title="Portfólio",
                   layout="wide",  # centered
                   page_icon="📊",
                   initial_sidebar_state="expanded",
                   menu_items={
                       'Get Help/Ajuda': 'https://www.extremelycoolapp.com/help',
                       'About': ""
                   }
                   )

st.title("Bem-vindo/a!")

