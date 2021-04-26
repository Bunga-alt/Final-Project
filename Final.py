"""
Author: Buyanbat Tamir
Date: 4/29/30
Data: Volcanoes
URL: https://share.streamlit.io/bunga-alt/final-project/main/Final.py
Description:

This program uses the Volcanoes database to create a bar chart, a histogram chart and map on streamlit.
The map uses the coordinates to mark where the volcanoes are located and show their name and their type.
The bar chart shows how many volcanoes are in the specific country using a frequency dictionary.
The histogram shows us how many times a volcano has erupted within a given timeframe.

"""

import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import plotly.express as px
@st.cache
#used by the pd.apply to change data in a dataframe
def eruption(x):
    if 'BCE' in x:
        x = x.strip('BCE')
        x = x.strip()
        x = int(x)*-1
    elif 'CE' in x:
        x = x.strip('CE')
        x = x.strip()
        x = int(x)
    return x


def bar_chart(df):
    st.title('Bar Chart of the frequency of volcanoes in a country')

    #Creating a frequency dictionary
    freq = {}
    countries = list(df['Country'])
    for x in countries:
        if x in freq:
            freq[x] += 1
        else:
            freq[x] = 1

    #sorting the dictionary by descending order
    sorted_dict = {}
    sorted_keys = sorted(freq, key=freq.get, reverse=True)
    for w in sorted_keys:
        sorted_dict[w] = freq[w]

    st.sidebar.header("Inputs for the Bar Chart")
    xmin = st.sidebar.selectbox('Select minimum amount of volcanoes', np.arange(0, 101,5))

    #creating a new dict with amounts higher than the user input
    new_dict = {}
    for w in sorted_dict:
        if sorted_dict[w] > xmin:
            new_dict[w] = sorted_dict[w]

    x = new_dict.keys()
    y = new_dict.values()

    fig = px.bar(x=x, y=y, color=y)
    st.plotly_chart(fig)


def histogram(df):
    st.title('Histogram Chart of the Last Known Eruptions')
    min_value = int(df['Last Known Eruption'].min())
    max_value = int(df['Last Known Eruption'].max())

    #Taking user inputs
    st.sidebar.header('Inputs for the Histogram')
    bin_input = st.sidebar.number_input('How many bins for the histogram', 5, 500)
    op = st.sidebar.selectbox('Select the opacity', np.arange(0.6, 1.01, 0.1))
    year = st.sidebar.number_input('Choose the year to start from',
                                   min_value=min_value,
                                   max_value=max_value)

    changed_df = df[df['Last Known Eruption'] > year]

    #Creating the hitogram
    fig = px.histogram(changed_df,
                       x='Last Known Eruption',
                       nbins=bin_input,
                       color=changed_df['Activity Evidence'],
                       opacity=op)
    st.plotly_chart(fig)


def main():

    df = pd.read_csv('volcanoes.csv')
    df.drop(['Link', 'Dominant Rock Type', 'Tectonic Setting', 'Region', 'Subregion'], axis=1, inplace=True)
    df = df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

    # Modifying the Last Known Eruption column to make it into an integer
    df['Last Known Eruption'] = df['Last Known Eruption'].apply(eruption)
    df = df[~df['Last Known Eruption'].str.contains('Unknown', na=False)]
    df['Last Known Eruption'] = df['Last Known Eruption'].astype(int)

    #Sorting the values by the modified column Last Known Eruption
    df.sort_values('Last Known Eruption', axis=0, ascending=True)

    st.title('Volcanoes Globally')
    st.dataframe(df)
    tool_tip = {'html': "Volcano Name: <br/> {Volcano Name} <br/> Volcano Type: <br/> <i>{Primary Volcano Type}<i>",
                'style': {"backgroundColor": 'steelblue',
                          "color": 'white'}
                }
    layer = pdk.Layer('ScatterplotLayer',
                      data=df,
                      get_position='[lon,lat]',
                      pickable=True,
                      get_radius=30000,
                      get_color=[0,0,0]
                      )
    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                   layers=[layer],
                   tooltip=tool_tip)
    st.pydeck_chart(map)

    histogram(df)

    bar_chart(df)


main()
