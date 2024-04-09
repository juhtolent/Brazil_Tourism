import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="Portfolio",
                   layout="wide",
                   page_icon="📊",
                   initial_sidebar_state="expanded"
                   )


# ----- dataframes and cache

# limpar o cache e atualizar as planilhas
# @st.cache_data.clear()

@st.cache_data
def import_category_2019():
    df_2019 = pd.read_excel(
        r"C:\Users\julia\Documents\GitHub\Brazil_Tourism\data\2019_MTur_Categorization.xlsx", header=3)
    
    #renaming to english and to standardize
    df_2019.rename({
        'UF': 'State',
        'Município': 'City',
        'Região Turística': 'Tourist Region',
        'Domésticos': 'Domestic Tourists',
        'Internacionais': 'International Tourists',
        'Estabelecimentos': 'Establishments', # Quantity of establishments related to tourism
        'Empregos': 'Jobs',  # Quantity of jobs related to tourism
        'Arrecadação de Impostos': 'Tax Revenue',
        'Categoria': 'Category',
        'Código Município': 'City Code'}, axis='columns', inplace=True)
    return df_2019


@st.cache_data
def import_category_2016():
    df_2016 = pd.read_csv(
        r"C:\Users\julia\Documents\GitHub\Brazil_Tourism\data\2016_MTur_Categorization.csv", delimiter=';')
    
    #renaming to english and to standardize
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
    
    #renaming to english and to standardize
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

## merge all columns and make filters
## decide which information is going to be where