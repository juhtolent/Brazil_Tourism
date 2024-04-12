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

    df_2017['International Tourists'] = df_2017['International Tourists'].replace(
        '.', '', regex=True)  # there are numbers with a "."
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

col1, col2 = st.columns([1, 2])
with col1:
    with st.container(border=True):
        st.markdown('''<h6 style='text-align: center;'>
                    Total number of cities classified
                    </h6>''', unsafe_allow_html=True)

        col11, col12, col13 = st.columns(3)
        with col11:
            value = len(df[df['Year'] == 2016])
            st.metric(label="2016", value=value)

        with col12:
            value = len(df[df['Year'] == 2017])
            delta = round((len(df[df['Year'] == 2017]) -
                           len(df[df['Year'] == 2016]))/len(df[df['Year'] == 2016])*100)
            st.metric(label="2017", value=value, delta=str(delta)+"%")

        with col13:
            value = len(df[df['Year'] == 2019])
            delta = round((len(df[df['Year'] == 2019]) -
                           len(df[df['Year'] == 2017]))/len(df[df['Year'] == 2017])*100)
            st.metric(label="2019", value=value, delta=str(delta)+"%")

        st.markdown('''Yearly data has varying city counts - In 2016, every Brazilian city was included (5570),
                    however there was a decline in subsequent years.
                    This means some cities have incomplete historical data. The reason for the variation
                    remains unclear and could not be found.''', unsafe_allow_html=True)

with col2:
    tab1, tab2 = st.tabs(['Zeros and Nulls', 'Headers'])

    with tab1:
        col21, col22 = st.columns([1.5, 1])

        with col21:
            with st.container():
                st.markdown('''Analysing the 2019 dataset,''',
                            unsafe_allow_html=True)
                columns = ['Jobs',
                           'Establishments',
                           'Domestic Tourists',
                           'International Tourists']

                st.dataframe(df[df['Year'] == 2019][columns]
                             .describe()
                             .loc[['count', 'min', '25%', '50%', '75%']])
                # quantitative

        with col22:
            fig = px.histogram(df[df['Year'] == 2019],
                               x='Establishments',
                               title='Establishments distribution in the 2019 database',
                               height=300
                               )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('''All cells of the year 2019 have information in them, there isn't a single null object in this dataset. 
                    However, on most columns, the lower quartile is 0, and also the histogram shows that a good chunk of the data is 0. 
                    Therefore, it seems that what would be null/empty was replaced by 0. Upon further analysis, 
                    this pattern persists across all historical datasets, suggesting that these zeros are intentional 
                    and hold meaning within the context of the data. It is also worth pointing out 
                    that all rows contain cities categorized as D and E, which are expected to have lower values.
                    ''', unsafe_allow_html=True)

    with tab2:
        table = [
            ['State', 'The state in which the city is located.'],
            ['City', 'The name of the city.'],
            ['Tourist Region', 'The designated tourist region the city belongs to.'],
            ['Domestic Tourists', 'The number of domestic tourists visiting the city.'],
            ['International Tourists',
                'The number of international tourists visiting the city.'],
            ['Jobs', 'The number of jobs available in the city.'],
            ['Tax Revenue', 'The amount of tax revenue generated by the city.'],
            ['Category', 'A classification assigned to the city based on specific economic performance of tourism in the municipalities.'],
            ['City Code', 'The official unique identifier for the city.'],
            ['Year', 'The year the data pertains to.'],
            ['Macro-Region', 'One of the five official regions of Brazil based on shared characteristics, like climate or vegetation.'],
        ]

        columns_explained = pd.DataFrame(
            table, columns=['Header', 'Definition'])

        st.dataframe(columns_explained)
# Category Analysis
st.markdown('''<h5 style> 2. Category Analysis </h5>''',
            unsafe_allow_html=True)

# Filtered boxplots
col1, space = st.columns([1, 3])
with col1:
    option = st.selectbox(
        'Select the year you would like to filter:',
        (2019, 2017, 2016))

st.markdown('''<h6 style='text-align: center;'>
            Distribution of each variable according to the categories
            </h6>''', unsafe_allow_html=True)

# first, the components to filter the df
df_chart = df[df['Year'] == option].sort_values('Category')

# function of boxplot


def boxplot(variable):
    fig = px.box(
        df_chart,
        x="Category",
        y=variable,
        template=template_dash,
        color="Category",
        width=500,
        height=350,
        color_discrete_sequence=colors
    )
    fig.update_layout(
        plot_bgcolor=bg_color_dash,
        title={
            'text': f"<b> {variable} </b>",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        })

    fig.update_traces(boxmean=True)

    return fig


col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(boxplot("Jobs"))
    st.plotly_chart(boxplot("Domestic Tourists"))

with col2:
    st.plotly_chart(boxplot("Establishments"))
    st.plotly_chart(boxplot("International Tourists"))

# ANALYSIS
st.markdown('''
            Looking at the numbers above, there are noteworthy trends that need to be discussed:

            1) <b> MEAN versus MEDIAN:</b> In this dataset, there is a significant distance between both metrics, signalizing that 
            there many outliers and internal groups that can be categorized.
            2)<b> OUTLIERS ON TOURIST DATA </b>: We see a few outliers, particularly for 
            domestic and international tourists. Further investigation is needed to determine 
            if these are data errors or represent genuinely high tourist volumes for specific cities.
            3) <b> HIGH INFRAESTRUCTURE CITIES </b>: Cities ranked A and B show a significantly 
            higher number of jobs and establishments compared to other categories. This suggests these cities have 
            a strong tourist infrastructure which is one of the primary focus of this analysis. 
            The larger range in category A data also indicates more variation in infrastructure within this group.
            4) <b> CATEGORIES D & E </b>: While categories D and E appear to have less interesting data initially. A close look shows that:
            - <b> CATEGORY D: </b> There are some outliers in terms of visitors and workers, but the number of establishments 
            is significantly distorted. This could indicate a data source error or that the city is genuinely not very interesting. I
            t is recommended to prioritize other cities when choosing a destination.
            - <b> CATEGORY E: </b> Almost all data points are 0, suggesting that these cities are likely not very interesting 
            for tourism. They may be considered for historical analysis, but they are not likely to be attractive destinations 
            for visitors.
            <br>
            ''', unsafe_allow_html=True)


# expander with cat D&E Analysis [[!!!!!]]
# 2 columns: yxy and cat stability
# end with filtering by location
