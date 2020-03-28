import csv
import sys
sys.path.append("..")

from fiadb import FIADB

client = FIADB(verbose=False)

acres_per_county = client.fullreport.get(
    reptype="State",
    snum="Area of sampled land and water, in acres",
    wc=552018,
    pselected="None",
    rselected="County code and name",
    cselected="EVALID",
)["row"]

acres = { c["content"][0:5] : int(c["column"][0]["cellValueNumerator"]) for c in (acres_per_county[1:]) }

# print(acres)

trees_per_county = client.fullreport.get(
    reptype="State",
    snum="Number of live trees (at least 1 inch d.b.h./d.r.c.), in trees, on forest land",
    wc=552018,
    pselected="Species group",
    rselected="County code and name",
    cselected="EVALID",
)["page"]

data = [ [ r["content"], [[c["content"][0:5], (0 if c["column"][0]["cellValueNumerator"] == "-" else (c["column"][0]["cellValueNumerator"] / acres[c["content"][0:5]] ))] for c in r["row"][1:] ] ] for r in trees_per_county]

for page in data[1:]:
  title = page[0]
  output_matrix = page[1]
  output_matrix.insert(0, ["FIPS", "PER_COUNTY"])

  with open("data/"+title+".csv", "w+", newline='') as output_csv:
    csvWriter = csv.writer(output_csv, delimiter=",")
    csvWriter.writerows(output_matrix)
