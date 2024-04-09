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
                       'About': info['About']
                   })

# ----- introduction
col1, col2 = st.columns([2, 8])

with col1:
    st.markdown(f'''<br> {info['Photo']}''', unsafe_allow_html=True)

with col2:
    st.title(f"Hi! I'm {info['Name']}!👋")
    st.caption(f"{info['Pronouns']}")
    st.markdown("I'm a data analyst with a passion for exploring and extracting insights from data. I've been working in the field of data analysis for the past two years, where I've gained valuable experience in various aspects of data science.")
    st.markdown("This portfolio showcases my skills in **data cleaning, analysis, and visualization**, in order to help you make data-driven decisions.")

# ----- credentials
    st.markdown(f'''
                [![Linkedin Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)]({
                info['Linkedin']})
                [![Github Badge](https://img.shields.io/badge/GitHub-100000?style=flat-square&logo=github&logoColor=white)]({
                info['Github']})
                [![Microsoft Outlook Badge](https://img.shields.io/badge/-Email-0078D4?style=flat-square&logo=microsoft-outlook&logoColor=white)](mailto:julia.mtolentino@hotmail.com{
                info['Email']})
                ''', unsafe_allow_html=True)

# ----- page explanation
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 🛫 Data Analysis and Dashboard")
        st.markdown(
            "This project tackles the question **:blue[Where should we travel to?]** by leveraging Brazil Tourism data analysis.he accompanying interactive dashboard allows users to filter and visualize travel options, empowering informed vacation planning. ")
        st.caption(
            "Skills showcased: Python [Pandas, Plotly, Seaborn], Data Visualization, Storytelling")

with col2:
    with st.container(border=True):
        st.markdown("### 🏙️ City record")
        st.markdown("🚧Under Construction🚧")
