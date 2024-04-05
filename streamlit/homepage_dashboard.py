import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from parameters import *
from st_pages import Page, Section, add_page_title, show_pages


st.set_page_config(page_title="Portfólio",
                   layout="wide",  # centered
                   page_icon="📊",
                   initial_sidebar_state="expanded",
                   menu_items={
                       'About': "I'm Julia, a data analyst passionate about extracting insights from data. This portfolio showcases my skills in data cleaning, analysis, and visualization, helping you make data-driven decisions."
                   })

with st.container():
    col1, col2 = st.columns([2, 8])

with col1:
    st.markdown(info['Photo'], unsafe_allow_html=True)

with col2:
    st.title("Hi! I'm Julia Tolentino!")
    st.markdown("I'm Julia, a data analyst with a passion for exploring and extracting insights from data. I've been working in the field of data analysis for the past two years, where I've gained valuable experience in various aspects of data science, including data cleaning, data wrangling, data visualization, and data modeling.")
    st.markdown("This portfolio showcases my skills in data cleaning, analysis, and visualization, helping you make data-driven decisions.")
