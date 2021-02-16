'''
Create two JSON files in /data/{FIPS}/ for each state; one based on 'species' data, and one based on 'species_group' data
'''

import csv
import sys
import json
import random
from pathlib import Path

sys.path.append("..")

import plotly
import plotly.express as px
import pandas as pd
from fiadb import FIADB

state_to_fips = {"GU": "66", "HI": "15", "DC": "11", "AK": "02", "AL": "01", "AR": "05", "AS": "60", "AZ": "04", "CA": "06", "CO": "08", "CT": "09", "DE": "10", "FL": "12", "GA": "13", "HI": "15", "IA": "19", "ID": "16", "IL": "17", "IN": "18", "KS": "20", "KY": "21", "LA": "22", "MA": "25", "MD": "24", "ME": "23", "MI": "26", "MN": "27", "MO": "29", "MS": "28", "MT": "30", "NC": "37", "ND": "38", "NE": "31", "NH": "33", "NJ": "34", "NM": "35", "NV": "32", "NY": "36", "OH": "39", "OK": "40", "OR": "41", "PA": "42", "PR": "72", "RI": "44", "SC": "45", "SD": "46", "TN": "47", "TX": "48", "UT": "49", "VA": "51", "VI": "78", "VT": "50", "WA": "53", "WI": "55", "WV": "54", "WY": "56"}
fips_to_state = {v: k for k, v in state_to_fips.items()}
client = FIADB()


def toFloat(f):
    try:
        return float(f)
    except:
        return 0


for STATE_PREFIX in state_to_fips:


    grouping = "species_group" # species | species_group
    grouping_cap = "Species group" # Species | "Species group"
    # STATE_PREFIX = "NY" # ca: 6, co: 8, mt: 30, ny: 36, wi: 55
    FIPS = state_to_fips[STATE_PREFIX]

    evalGrps = client.evalgrp.get(whereClause=f"STATECD IN ({FIPS})", mostRecent="Y")
    if isinstance(evalGrps, list):
        evalGrp = evalGrps[-1]
    elif isinstance(evalGrps, int):
        evalGrp = evalGrps
    else:
        sys.exit(f"Invalid evalGrp query results for {STATE_PREFIX}")

    if evalGrp == "Empty evalGrp query results":
        print(f"Empty evalGrp query results for {STATE_PREFIX}")
        continue

    acres_per_county = client.fullreport.get(
        reptype="State",
        snum="Area of sampled land and water, in acres",
        wc=str(evalGrp),
        pselected="None",
        rselected="County code and name",
        cselected="EVALID",
    )["row"]

    acres = {
        c["content"][0:5]: c["column"][0]["cellValueNumerator"]
        for c in (acres_per_county[1:])
    }

    trees_per_county = client.fullreport.get(
        reptype="State",
        snum="Number of live trees (at least 1 inch d.b.h./d.r.c.), in trees, on forest land",
        wc=str(evalGrp),
        pselected=grouping_cap,  # For more grouping, less descriptive names: "Species group"; or for more specificity: "Species"
        rselected="County code and name",
        cselected="EVALID",
    )["page"]


    data = {
        page["content"]: {
            col["content"][0:5]: toFloat(col["column"][0]["cellValueNumerator"])
            for col in (page["row"][1:])
        }
        for page in trees_per_county
    }

    state_data = { "dataset": str(evalGrp), "results": {}}
    counter = 0
    for page in data:
        title = "All trees" if page == "Page total" else page.replace("/", " or ")
        # output_matrix = [["FIPS", "PER_COUNTY"]]
        output_matrix = {}
        for county in acres:
            try:
                # output_matrix.append([county, data[page][county] / acres[county]])
                output_matrix[county] = round(data[page][county] / acres[county], 3)
            except KeyError:
                counter += 1
                output_matrix[county] = 0

        state_data["results"][title] = output_matrix


    Path(f"data/{FIPS}/").mkdir(parents=True, exist_ok=True)

    with open(f'data/{FIPS}/{grouping}.json', 'w+') as outfile:
        json.dump(state_data, outfile)
    print(f"{counter} errors for {STATE_PREFIX}")
        



for STATE_PREFIX in state_to_fips:

    grouping = "species" # species | species_group
    grouping_cap = "Species" # Species | "Species group"
    # STATE_PREFIX = "NY" # ca: 6, co: 8, mt: 30, ny: 36, wi: 55
    FIPS = state_to_fips[STATE_PREFIX]

    evalGrps = client.evalgrp.get(whereClause=f"STATECD IN ({FIPS})", mostRecent="Y")
    if isinstance(evalGrps, list):
        evalGrp = evalGrps[-1]
    elif isinstance(evalGrps, int):
        evalGrp = evalGrps
    else:
        sys.exit(f"Invalid evalGrp query results for {STATE_PREFIX}")

    if evalGrp == "Empty evalGrp query results":
        print(f"Empty evalGrp query results for {STATE_PREFIX}")
        continue

    acres_per_county = client.fullreport.get(
        reptype="State",
        snum="Area of sampled land and water, in acres",
        wc=str(evalGrp),
        pselected="None",
        rselected="County code and name",
        cselected="EVALID",
    )["row"]

    acres = {
        c["content"][0:5]: c["column"][0]["cellValueNumerator"]
        for c in (acres_per_county[1:])
    }

    trees_per_county = client.fullreport.get(
        reptype="State",
        snum="Number of live trees (at least 1 inch d.b.h./d.r.c.), in trees, on forest land",
        wc=str(evalGrp),
        pselected=grouping_cap,  # For more grouping, less descriptive names: "Species group"; or for more specificity: "Species"
        rselected="County code and name",
        cselected="EVALID",
    )["page"]


    data = {
        page["content"]: {
            col["content"][0:5]: toFloat(col["column"][0]["cellValueNumerator"])
            for col in (page["row"][1:])
        }
        for page in trees_per_county
    }

    state_data = { "dataset": str(evalGrp), "results": {}}
    counter = 0
    for page in data:
        title = "All trees" if page == "Page total" else page.replace("/", " or ")
        # output_matrix = [["FIPS", "PER_COUNTY"]]
        output_matrix = {}
        for county in acres:
            try:
                output_matrix[county] = round(data[page][county] / acres[county], 3)
            except KeyError:
                counter += 1
                output_matrix[county] = 0

        state_data["results"][title] = output_matrix

    with open(f'data/{FIPS}/{grouping}.json', 'w+') as outfile:
        json.dump(state_data, outfile)