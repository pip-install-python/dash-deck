"""
Adapted from: https://pydeck.gl/gallery/s2_layer.html

Plot of values for a particular S2 ID in the S2 geohashing scheme.

This example is adapted from the deck.gl documentation.
"""

import os

import dash
import dash_deck
from dash import html
import pydeck as pdk
import pandas as pd

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")


import pydeck as pdk
import pandas as pd

S2_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf.s2cells.json"  # noqa

df = pd.read_json(S2_LAYER_DATA)

# Define a layer to display on a map
layer = pdk.Layer(
    "S2Layer",
    df,
    pickable=True,
    wireframe=False,
    filled=True,
    extruded=True,
    elevation_scale=1000,
    getS2Token="token",
    get_fill_color="[value * 255, (1 - value) * 255, (1 - value) * 128]",
    get_elevation="value",
)

# Set the viewport location
view_state = pdk.ViewState(
    latitude=37.7749295, longitude=-122.4194155, zoom=11, bearing=0, pitch=45
)

# Render
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
)


app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(),
        id="deck-gl",
        tooltip={"text": "{token} value: {value}"},
        mapboxKey=mapbox_api_token,
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)
