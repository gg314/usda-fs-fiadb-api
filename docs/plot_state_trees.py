from urllib.request import urlopen
import glob
import json
import re
import pandas as pd

# import plotly.express as px
# from subprocess import call
import plotly

state_prefix = "mt"


# I am having trouble getting orca to start, so I run a server with `orca serve --port 51110 --debug` and then execute the Python code
plotly.io.orca.config.port = 51110
print(plotly.io.orca.config)
print(plotly.io.orca.status)


# JSON boundaries come from urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json")
# with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
with open("./geojson-counties-fips.json") as response:
    counties = json.load(response)


counter = 0
files = glob.glob("data/" + state_prefix + "_*.csv")
for filename in files:
    counter += 1

    match = re.search((state_prefix + "_(.*).csv"), filename)
    if match:

        import plotly.express as px

        df = pd.read_csv(filename, dtype={"FIPS": str})

        print("Saving %s" % match.group(1))

        # California: {"lat": 37.216, "lon": -119.72}, width="700", height="1050",
        # Colorado:  {"lat": 39.14, "lon": -105.33}, width="?", height="?",
        # Montana:  {"lat": 47.217, "lon": -110.087}, width="?", height="?",
        # Wisconsin:  {"lat": 44.8, "lon": -89.4173}, width="750", height="650",

        lbl = "PER_COUNTY"
        fig = px.choropleth_mapbox(
            df,
            geojson=counties,
            locations="FIPS",
            color=lbl,
            color_continuous_scale="tempo",  # "mint" or others
            zoom=5.4,
            center={"lat": 47.217, "lon": -110.087},
            opacity=1,
            labels={lbl: match.group(1) + " per acre"},
            mapbox_style="white-bg",  # "carto-positron"
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(
            {
                "title": {
                    "text": match.group(1),
                    "font": {"size": 38, "family": "Harmonia Sans Pro"},
                    "x": 0.46,
                    "y": 0.93,
                    "xanchor": "center",
                    "yanchor": "top",
                }
            }
        )
        fig.update_coloraxes(showscale=False)
        fig.update_layout(showlegend=False)

        #      fig.show() # show interactive figure in browser
        fig.write_image(
            file="./results/" + state_prefix + "_" + match.group(1) + ".png",
            format="png",
            width="750",
            height="650",
            validate=False,
        )
        print("Saved %s (%d/%d)" % (match.group(1), counter, len(files)))
