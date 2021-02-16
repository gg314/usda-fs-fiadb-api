'''
A helper script to split apart some GeoJSON and to list some state <option> HTML
'''

import json
import sys

state_to_fips = {"AK": "02", "AL": "01", "AR": "05", "AS": "60", "AZ": "04", "CA": "06", "CO": "08", "CT": "09", "DC": "11", "DE": "10", "FL": "12", "GA": "13", "GU": "66", "HI": "15", "IA": "19", "ID": "16", "IL": "17", "IN": "18", "KS": "20", "KY": "21", "LA": "22", "MA": "25", "MD": "24", "ME": "23", "MI": "26", "MN": "27", "MO": "29", "MS": "28", "MT": "30", "NC": "37", "ND": "38", "NE": "31", "NH": "33", "NJ": "34", "NM": "35", "NV": "32", "NY": "36", "OH": "39", "OK": "40", "OR": "41", "PA": "42", "PR": "72", "RI": "44", "SC": "45", "SD": "46", "TN": "47", "TX": "48", "UT": "49", "VA": "51", "VI": "78", "VT": "50", "WA": "53", "WI": "55", "WV": "54", "WY": "56"}
fips_to_state = {v: k for k, v in state_to_fips.items()}
long_to_state = {'Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC','Florida': 'FL','Georgia': 'GA','Guam': 'GU','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Puerto Rico': 'PR','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}
state_to_long = {v: k for k, v in long_to_state.items()}

print(state_to_long.keys() - state_to_fips.keys())
print(state_to_fips.keys() - state_to_long.keys())
print("---")
for s in state_to_fips:
    print(f"<option value='{state_to_fips[s]}' data-state='{s}'>{state_to_long[s]}</option>")

# JSON boundaries come from urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json")
with open("./geojson-counties-fips.json") as response:
    counties = json.load(response)

for state in state_to_fips:
    fips = state_to_fips[state]
    ii = 0
    feature_collection = {"type": "FeatureCollection", "features": []}
    for k in counties["features"]:
        if (k["properties"]["STATE"]) == fips:
            feature_collection["features"].append( k )
            ii += 1
        
    with open(f'geojson/counties-{fips}.geojson', 'w') as f:
        json.dump(feature_collection, f)
    print(f"Added {ii} counties for {fips_to_state[fips]}")

