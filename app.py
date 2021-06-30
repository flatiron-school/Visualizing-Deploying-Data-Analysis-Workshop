# Imports
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Explore Austin's Animal Shelter Data")

# Read in our data
df = pd.read_csv("data/Austin_Animal_Center_Intakes_061521_with_location_details.csv", 
                 parse_dates=['DateTime'])

# Adding date subset functionality in the sidebar
# First getting the minimum and maximum dates out of our data
date_min = df['DateTime'].min()
date_max = df['DateTime'].max()
# Then creating an input option
range_min, range_max = st.sidebar.date_input(label="What time frame would you like to explore?", 
                                             value=[date_min, date_max], 
                                             min_value=date_min,
                                             max_value=date_max)
# Need to update the type to match with pandas
range_min = pd.to_datetime(range_min)
range_max = pd.to_datetime(range_max)                                     
# Based on the above input, charts will only show details from that timeframe
sub_df = df.loc[(df['DateTime'] <= range_max) &
                (df['DateTime'] >= range_min)]

# Adding an input option to the sidebar to toggle between visuals
viz_option = st.sidebar.selectbox(label='Which data would you like to explore?',
                                  options =['Types of Animal Intakes', 
                                            'Animal Intakes Over Time', 
                                            'Found Locations of Animals'])

# Visualizing our animal types
if viz_option == 'Types of Animal Intakes':
    st.header('Types of Animal Intakes')
    # Building our types data
    sub_df['Animal Type'] = sub_df['Animal Type'].replace({'Bird': 'Other', 'Livestock': 'Other'})
    types = sub_df['Animal Type'].value_counts().reset_index()
    types = types.rename(columns={'index':'Type', 'Animal Type': 'Count'})
    # Visualizing our types data
    fig1 = px.pie(types, values='Count', names='Type',
                color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig1)

# Visualizing our trends over time
if viz_option == 'Animal Intakes Over Time':
    st.header('Animal Intakes Over Time')
    # Building our types data
    sub_df['Year'] = sub_df['DateTime'].dt.year
    sub_df['Month'] = sub_df['DateTime'].dt.month
    annual_trend = sub_df.groupby(['Year', 'Month']).count()['Animal ID'].reset_index()
    # Visualizing our trends data
    fig2 = px.line(annual_trend, y='Animal ID', x='Month', color='Year',
                labels={'Animal ID': 'Number of Animal Intakes'}) # better x label for clarity
    st.plotly_chart(fig2)

# Mapping our intakes
if viz_option == 'Found Locations of Animals':
    st.header('Found Locations of Animals')
    # Building our location data
    location_df = sub_df.loc[sub_df['Found Zipcode'].isna() == False]
    location_count = location_df.groupby(by=['Found Location', 
                                            'Found Latitude', 
                                            'Found Longitude']).count()['Animal ID'].reset_index()
    location_count = location_count.rename(columns={'Animal ID':'Count'})
    # Visualizing our location data
    fig3 = px.scatter_mapbox(location_count, lat="Found Latitude", lon="Found Longitude",
                            color="Count", size="Count",zoom=10,
                            hover_name='Found Location')
    fig3.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig3)