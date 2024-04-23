import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import json
import locale

st.set_page_config(page_title='Dashboard',
                   layout='wide',
                   page_icon='📊',
                   initial_sidebar_state='expanded'
                   )

# ----- dataframes and cache


@st.cache_data
def import_category_2019():
    df_2019 = pd.read_excel('data/2019_MTur_Categorization.xlsx', header=3)

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
        'MACRO': 'MacroRegion',
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
        'Macro Região': 'MacroRegion',
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

# 2019 data doesn't have the column "MacroRegion", will added below


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


# assigning each row a MacroRegion
df['MacroRegion'] = df['State'].apply(set_macro_region)

# assigning a number to each category


def category_number(category):
    if category == 'A':
        return 4
    elif category == 'B':
        return 3
    elif category == 'C':
        return 2
    elif category == 'D':
        return 1
    else:
        return 0


df['Category Number'] = df['Category'].apply(category_number)

# ----- filters
with st.sidebar:

    st.title('Filters')

    macro_region = st.multiselect(
        'Select a MacroRegion:',
        options=df[df['Year'] == 2019]['MacroRegion'].sort_values().unique(),
        default=df[df['Year'] == 2019]['MacroRegion'].sort_values().unique(),
        placeholder='No options selected',
        help="The Brazilian government has grouped the country's states into five large geographic and statistical units called the Major Regions (Grandes Regiões): North (Norte), Northeast (Nordeste), Central-West (Centro-Oeste), Southeast (Sudeste), and South (Sul)."
    )

    df = df.query("MacroRegion == @macro_region")

    state = st.multiselect(
        'Select a State:',
        options=df[df['Year'] == 2019]['State'].sort_values().unique(),
        default=df[df['Year'] == 2019]['State'].sort_values().unique(),
        placeholder='No options selected'
    )

    df = df.query("State == @state")

if len(df) == 0:
    st.error('Select at least one Macro-Region and State', icon="🚨")
else:
    # ----- metrics/ big numbers
    st.title("Tourism Map Dashboard (2019)")
    col = st.columns([1, 2, 1, 1])

    # localize number format to en
    locale.setlocale(locale.LC_ALL, '')

    with col[0]:
        st.metric(label='Quantity of cities',
                  value=len(df[df['Year'] == 2019]['City'].unique()))
    with col[1]:
        metric_tax_revenue = locale.format_string('%.0f',
                                                  val=df[df['Year'] ==
                                                         2019]['Tax Revenue'].sum(),
                                                  grouping=True,
                                                  monetary=False)

        st.metric(label='Tax Revenue in 2019',
                  value=f'R$ {metric_tax_revenue}')

    with col[2]:
        st.metric(label='Establishments',
                  value=df[df['Year'] == 2019]['Establishments'].sum().astype(int))

    with col[3]:
        st.metric(label='Jobs',
                  value=df[df['Year'] == 2019]['Jobs'].sum().astype(int))

    # ----- charts
    col = st.columns([2, 1])

    with col[0]:
        # ----- choropleth / brazil map
        @st.cache_data
        def import_geojson():
            geojson = json.load(
                open('data\brasil_estados.json'))
            return geojson

        geojson = import_geojson()

        df_choropleth = pd.pivot_table(df,
                                       values='Category Number',
                                       index='State',
                                       aggfunc='sum')

        fig = px.choropleth(df_choropleth, geojson=geojson,
                            locations=df_choropleth.index,
                            color='Category Number',
                            range_color=(
                                0, max(df_choropleth['Category Number'])),
                            scope='south america',
                            color_continuous_scale='Agsunset_r'
                            )

        fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)',
                                   projection_scale=1.75,
                                   center=dict(lat=-15, lon=-55)),
                          coloraxis_colorbar_x=-0.1,
                          title={
            'text': '<b> States with more well categorized cities </b>',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    with col[1]:
        # ----- top cities in according to tax revenue
        with st.popover("Change ranking column"):
            variable = st.selectbox("Which variable to rank?",
                                    options=['Tax Revenue',
                                             'Domestic Tourists',
                                             'International Tourists',
                                             'Jobs',
                                             'Establishments'])

        df_cities_tax = df[df['Year'] == 2019][[
            'City', variable]].sort_values(by=variable, ascending=False)

        st.dataframe(df_cities_tax,
                     column_config={
                         variable: st.column_config.ProgressColumn(
                             variable,
                             format="%f",
                             min_value=0,
                             max_value=max(df_cities_tax[variable]))},
                     hide_index=True,
                     use_container_width=True)

    # ----- heatmap
    df_heatmap = pd.pivot_table(data=df,
                                values='Category Number',
                                index='Year',
                                columns=['State'],
                                fill_value=0,
                                aggfunc='sum')

    fig = px.imshow(df_heatmap.sort_values(by='State', axis=1),
                    text_auto=True,
                    color_continuous_scale='Agsunset_r',
                    aspect='auto')

    fig.update_layout(xaxis=dict(title='Category in 2019',
                                 side='bottom'),
                      yaxis=dict(type='category'),
                      autosize=False,
                      title={
        'text': '<b> States with more well categorized cities through the years </b>',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )

    st.plotly_chart(fig, use_container_width=True)
