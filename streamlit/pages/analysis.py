import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import io


st.set_page_config(page_title="Portfolio",
                   layout="wide",
                   page_icon="📊",
                   initial_sidebar_state="collapsed"
                   )


# ----- dataframes and cache

@st.cache_data
def import_category_2019():
    df_2019 = pd.read_excel(
        r"C:\Users\julia\Documents\GitHub\Brazil_Tourism\data\2019_MTur_Categorization.xlsx", header=3)

    # renaming to english and to standardize
    df_2019.rename({
        'UF': 'State',
        'Município': 'City',
        'Região Turística': 'Tourist Region',
        'Domésticos': 'Domestic Tourists',
        'Internacionais': 'International Tourists',
        # Quantity of establishments related to tourism
        'Estabelecimentos': 'Establishments',
        'Empregos': 'Jobs',  # Quantity of jobs related to tourism
        'Arrecadação de Impostos': 'Tax Revenue',
        'Categoria': 'Category',
        'Código Município': 'City Code'}, axis='columns', inplace=True)
    return df_2019


df_2019 = import_category_2019()


@st.cache_data
def import_category_2016():
    df_2016 = pd.read_csv(
        r"C:\Users\julia\Documents\GitHub\Brazil_Tourism\data\2016_MTur_Categorization.csv", delimiter=';')

    # renaming to english and to standardize
    df_2016.rename({
        # the five official regions of Brazil based on shared characteristics, like climate or vegetation.
        'MACRO': 'Macro-Region',
        'UF': 'State',
        'MUNICIPIO': 'City',
        'REGIAO_TURISTICA': 'Tourist Region',
        'QUANTIDADE_VISITAS_ESTIMADA_NACIONAL': 'Domestic Tourists',
        'QUANTIDADE_VISITAS_ESTIMADA_INTERNACIONAL': 'International Tourists',
        'QUANTIDADE_ESTABELECIMENTOS': 'Establishments',
        'QUANTIDADE_EMPREGOS': 'Jobs',
        'CLUSTER': 'Category',
        'CODIGO_MUNICIPIO': 'City Code'}, axis='columns', inplace=True)
    return df_2016


df_2016 = import_category_2016()


@st.cache_data
def import_category_2017():
    df_2017 = pd.read_csv(
        r"C:\Users\julia\Documents\GitHub\Brazil_Tourism\data\2017_MTur_Categorization.csv", delimiter=';')

    # renaming to english and to standardize
    df_2017.rename({
        'Macro Região': 'Macro-Region',
        'UF': 'State',
        'Município': 'City',
        'Região': 'Tourist Region',
        'Demanda Doméstica': 'Domestic Tourists',
        'Demanda Internacional': 'International Tourists',
        'Qtd. Estabelecimentos Hospedagem': 'Establishments',
        'Qtd. Empregos Hospedagem': 'Jobs',
        'Cluster 2017 (Categoria)': 'Category',
        'Código Município': 'City Code'}, axis='columns', inplace=True)
    return df_2017


df_2017 = import_category_2017()

# adding a column to each df and concating the dataframes
df_2019['Year'] = 2019
df_2016['Year'] = 2016
df_2017['Year'] = 2017

df = pd.concat([df_2019, df_2016, df_2017])

# ---- general settings for charts
template_dash = "plotly_white"
bg_color_dash = "rgba(0,0,0,0)"
colors = ['#003f5c', '#374c80', '#7a5195',
          '#bc5090', '#ef5675', '#ed9231', '#f2ff49']


########## Analysis Main Panel ########

# Title
st.markdown('''<h2 style = "text-align: center;"><span style="word-wrap:break-word;">
                    🛫Where should we travel to?
                </span> </h2>''', unsafe_allow_html=True)
st.caption(f'''This portfolio project showcases my expertise in data analysis through answering the question:
           "Which Brazilian cities should we travel to?". This is done by an examination of Brazilian
           cities identified by the Brazilian Ministry of Tourism as key destinations
           in their public policy plan (Mapa do Turismo/Tourism Map).
           This analysis is also explored in a [jupyter notebook](https://github.com/juhtolent/Brazil_Tourism/blob/main/Data%20Analysis%20-%20Tourism.ipynb)
           available in this streamlit's repository.''')


# Quick Explanation
with st.expander("Quick explanation about the Tourism Map"):
    st.markdown('''<h5 style> Tourism Map </h5>''', unsafe_allow_html=True)
    st.markdown('''The Brazilian Tourism Map is an instrument within the Tourism Regionalization 
                Program that defines the area - territorial cut - to be worked on as a priority 
                by the Ministry of Tourism within the scope of public policy development. 
                In addition, the municipalities are categorized in order to identify the 
                performance of the sector's economy in the municipalities based on five variables crossed 
                in a categorization.''', unsafe_allow_html=True)
    st.markdown('''<br> <h5 style> The Categorization of Tourist Municipalities </h5>''',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            The [Categorization of Municipalities](http://www.regionalizacao.turismo.gov.br/images/conteudo/Perguntas_espostas_Categorizacao_2019.pdf) is based on a set of indicators that measure the 
            economic performance of tourism in the municipalities, such as:
            - The number of tourist arrivals
            - The number of tourist nights
            - The revenue generated by tourism
            - The number of jobs generated by tourism
                  
            This Categorization has three historical versions available: 2016, 2017 and 2019.
            ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''                    
                    | Category | Meaning |
                    |--|--------------------------------|
                    |A | Emerging Tourist Municipalities|
                    |B | Developing Tourist Municipalities|
                    |C | Consolidating Tourist Municipalities|
                    |D | Tourist Municipalities of National Interest|
                    |E | Tourist Municipalities of International Interest| 
                    <br>
                    ''', unsafe_allow_html=True)

# database overall characteristics

st.markdown('''<h5 style> 1. Overall database overview </h5>''',
            unsafe_allow_html=True)
col1, col2 = st.columns([1, 3])
with col1:
    with st.container(border=True):
        st.markdown('''<h6 style='text-align: center;'> 
                    Total number of cities classified 
                    </h6>''', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="2019", value=len(df[df['Year'] == 2019]))

        with col2:
            st.metric(label="2017", value=len(df[df['Year'] == 2017]))

        with col3:
            st.metric(label="2016", value=len(df[df['Year'] == 2016]))

# st.table(df.describe())
