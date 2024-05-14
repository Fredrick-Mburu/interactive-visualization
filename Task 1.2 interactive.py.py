#!/usr/bin/env python
# coding: utf-8

# **MyInteractiveUFOVisualization**

# In[8]:


import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

# Load your data
df = pd.read_csv('scrubbed.csv', low_memory=False)  # Adjust path as necessary

# Handle data types specifically for problematic columns
# Convert datetime to pandas datetime object and extract year
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')  # Coerce errors will set invalid parsing as NaT
df['year'] = df['datetime'].dt.year  # Extract year

# Strip any trailing whitespace from the column names
df.columns = df.columns.str.strip()

# Create a more descriptive, two-line title
title_text = ("Exploring UFO Sightings Globally:<br>An Interactive Visualization of Locations, Shapes, "
              "and Durations from 1947 to Present")

# Generate the scatter geo plot with the detailed design
fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='shape',
                     hover_name='city', hover_data={'state': True, 'datetime': True, 'duration (seconds)': True},
                     animation_frame='year', projection="natural earth", title=title_text)

# Update layout for better presentation
fig.update_layout(
    legend_title_text='UFO Shapes',
    legend_orientation="h",
    legend_title_font_color="blue",
    margin={"r":0, "t":50, "l":0, "b":0},
    geo=dict(
        scope='world',  # Can be changed to 'north america' or other regions
        landcolor='rgb(217, 217, 217)',
        lakecolor='rgb(255, 255, 255)',
        showland=True,
        countrycolor='rgb(204, 204, 204)'
    )
)

# Enhance interactivity with additional layout options
fig.update_geos(
    coastlinecolor="RebeccaPurple",
    showcountries=True,
    countrycolor="RebeccaPurple"
)

# Initialize the Dash app (replace '__name__' with the name of your app if needed)
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(figure=fig),
    html.P("Explore the map to see UFO sightings across different regions and times.")
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)

