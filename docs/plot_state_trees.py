from urllib.request import urlopen
import glob
import json
import re
import pandas as pd

import plotly.express as px
from subprocess import call
import plotly



plotly.io.orca.config.port = 51111
print(plotly.io.orca.config)
print(plotly.io.orca.status)


# JSON boundaries come from urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json")
with open("./geojson-counties-fips.json") as response:
    counties = json.load(response)


counter = 0
files = glob.glob("./data/co_*.csv")
for filename in files:
    counter += 1
    match = re.search(r"co_(.*)\.csv", filename)
    if match:
        df = pd.read_csv(filename, dtype={"FIPS": str})


        lbl = "PER_COUNTY"
        fig = px.choropleth_mapbox(
            df,
            geojson=counties,
            locations="FIPS",
            color=lbl,
            color_continuous_scale="Blugrn",
            zoom=5.4,
            center={"lat": 39.7, "lon": -104.99},
            opacity=1,
            labels={lbl: match.group(1) + " per acre"},
            mapbox_style="white-bg",  # "carto-positron"
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout({"title": {"text": match.group(1), "font": {"size": 38, "family": "Harmonia Sans Pro"}, 'x': 0.46, 'y': 0.85, 'xanchor': 'center', 'yanchor': 'top'}})
        fig.update_coloraxes(showscale=False)
        fig.update_layout(showlegend=False)

        #fig.show()
        fig.write_image(file="./results/co_"+match.group(1)+".png", format="png", width="750", height="575", validate=True)
        print("Saved %s (%d/%d)" % (match.group(1), counter, len(files)))
