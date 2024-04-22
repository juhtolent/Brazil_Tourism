import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Dashboard',
                   layout='wide',
                   page_icon='📊',
                   initial_sidebar_state='expanded'
                   )

# ----- dataframes and cache


@st.cache_data
def import_category_2019():
    df_2019 = pd.read_excel(
        filepath, header=3)

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
        'data/2016_MTur_Categorization.csv', delimiter=';')

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
        'data/2017_MTur_Categorization.csv', delimiter=';')

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

    df_2017['International Tourists'] = df_2017['International Tourists'].replace(
        '.', '', regex=True)  # there are numbers with a '.'
    df_2017['International Tourists'] = pd.to_numeric(
        df_2017['International Tourists'])

    df_2017['Domestic Tourists'] = df_2017['Domestic Tourists'].replace(
        '.', '', regex=True)
    df_2017['Domestic Tourists'] = pd.to_numeric(df_2017['Domestic Tourists'])

    return df_2017


df_2017 = import_category_2017()

# adding a column to each df and concating the dataframes
df_2019['Year'] = 2019
df_2016['Year'] = 2016
df_2017['Year'] = 2017

df = pd.concat([df_2019, df_2016, df_2017])


@st.cache_data
def import_latlong():
    # adding lat/long to the dataframe
    df_latlong = pd.read_csv(
        'data/BR_cities_latlong.csv', delimiter=',')

    # renaming to english and to standardize
    # renaming to english and to standardize
    df_latlong.rename({
        'codigo_ibge': 'City Code',
        'nome': 'City',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'capital': 'Is Capital City',  # each state has a capital in Brazil,
        'codigo_uf': 'State Code',
        'siafi_id': 'Siafi ID',  # code for government administrative processes
        'ddd': 'Area Code',
        'fuso_horario': 'Time Zone'
    }, axis='columns', inplace=True)
    return df_latlong


df_latlong = import_latlong()

# merging both dfs
df = pd.merge(df,
              # selecting only lat/long information
              df_latlong[['City Code', 'latitude', 'longitude']],
              how='left',
              on='City Code')

# 2019 data doesn't have the column "macro-region", will add below


def set_macro_region(state):
    if state in ['AL', 'BA', 'MA', 'CE', 'PB', 'PE', 'PI', 'RN', 'SE']:
        return 'Nordeste'
    elif state in ['MG', 'SP', 'RJ', 'ES']:
        return 'Sudeste'
    elif state in ['RS', 'SC', 'PR']:
        return 'Sul'
    elif state in ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO']:
        return 'Norte'
    elif state in ['GO', 'MT', 'DF', 'MS']:
        return 'Centro-Oeste'


# assigning each row a macro-region
df['Macro-Region'] = df['State'].apply(set_macro_region)

# ----- filters
with st.sidebar:
    macro_region = st.selectbox(
        'Select a Macro-Region:',
        options=df[df['Year'] == 2019].sort_values().unique(),
        index=None,
        placeholder='All Macro-regions selected',
        help="The Brazilian government has grouped the country's states into five large geographic and statistical units called the Major Regions (Grandes Regiões): North (Norte), Northeast (Nordeste), Central-West (Centro-Oeste), Southeast (Sudeste), and South (Sul)."
    )

    df = df.query("Macro-Region == @macro_region")

    state = st.selectbox(
        'Select a State:',
        options=df[df['Year'] == 2019].sort_values().unique(),
        index=None,
        placeholder='All States selected'
    )

    df = df.query("State == @state")

st.dataframe(df)
