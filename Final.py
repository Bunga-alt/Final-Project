"""
Author: Buyanbat Tamir
Date: 4/29/30
Description: 2 queries and a map using the volcanoes database

"""

import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import plotly.express as px

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


def histogram(df):
    st.title('Histogram Chart')
    min_value = int(df['Last Known Eruption'].min())
    max_value = int(df['Last Known Eruption'].max())
    st.sidebar.header('Inputs for the Histogram')
    bin_input = st.sidebar.number_input('How many bins for the histogram', 1, 500)

    year = st.sidebar.number_input('Choose the year to start from',
                             min_value=min_value,
                             max_value=max_value,)
    button = st.sidebar.button("Press to see the changes")

    changed_df = df[df['Last Known Eruption'] > year]

    if button:
        fig = px.histogram(changed_df,
                           x='Last Known Eruption',
                           nbins=bin_input,
                           color=changed_df['Activity Evidence'],
                           opacity=0.7)
        st.plotly_chart(fig)


def main():

    df = pd.read_csv('volcanoes.csv')
    df.drop(['Link','Dominant Rock Type','Tectonic Setting','Region','Subregion'], axis=1, inplace=True)
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


main()
