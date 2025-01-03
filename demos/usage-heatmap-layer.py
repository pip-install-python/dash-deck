"""
Adapted from: https://pydeck.gl/gallery/heatmap_layer.html

Location of livestock raised in New Mexico in the United States in 2006,
via the United Nations and FAOSTAT, with the source data viewable here: 
http://www.fao.org/faostat/en/

Locations for poultry are viewable in blue and cattle are in orange.

Overlaid with the satellite imagery from Mapbox to highlight the how 
terrain affects agriculture.

"""

import os

import dash
import dash_deck
from dash import html
import pydeck as pdk
import pandas as pd

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")


CATTLE_DATA = (
    "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/nm_cattle.csv"
)
POULTRY_DATA = (
    "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/nm_chickens.csv"
)


HEADER = ["lng", "lat", "weight"]
cattle_df = pd.read_csv(CATTLE_DATA, header=None).sample(frac=0.5)
poultry_df = pd.read_csv(POULTRY_DATA, header=None).sample(frac=0.5)

cattle_df.columns = HEADER
poultry_df.columns = HEADER

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]


view = pdk.data_utils.compute_view(cattle_df[["lng", "lat"]])
view.zoom = 6

cattle = pdk.Layer(
    "HeatmapLayer",
    data=cattle_df,
    opacity=0.9,
    get_position=["lng", "lat"],
    aggregation='"MEAN"',
    color_range=COLOR_BREWER_BLUE_SCALE,
    threshold=1,
    get_weight="weight",
    pickable=True,
)

poultry = pdk.Layer(
    "HeatmapLayer",
    data=poultry_df,
    opacity=0.9,
    get_position=["lng", "lat"],
    threshold=0.75,
    aggregation='"MEAN"',
    get_weight="weight",
    pickable=True,
)


r = pdk.Deck(
    layers=[cattle, poultry],
    initial_view_state=view,
)

app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(),
        id="deck-gl",
        tooltip={
            "text": "Concentration of cattle in blue, concentration of poultry in orange"
        },
        mapboxKey=mapbox_api_token,
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)
