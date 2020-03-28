from urllib.request import urlopen
import glob
import json
import re
import pandas as pd

with urlopen(
    "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
) as response:
    counties = json.load(response)

for filename in glob.glob("./data/*.csv"):
    match = re.search("\\\(.*)\.csv", filename)
    if match:
        df = pd.read_csv(filename, dtype={"FIPS": str})

        import plotly.express as px

        lbl = "PER_COUNTY"
        fig = px.choropleth_mapbox(
            df,
            geojson=counties,
            locations="FIPS",
            color=lbl,
            color_continuous_scale="Blugrn",
            zoom=5.4,
            center={"lat": 45.0, "lon": -89.0},
            opacity=1,
            labels={lbl: match.group(1) + " per acre"},
            mapbox_style="white-bg",  # "carto-positron"
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.show()
