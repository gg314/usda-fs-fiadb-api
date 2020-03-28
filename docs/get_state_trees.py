import csv
import sys

sys.path.append("..")

from fiadb import FIADB


def toFloat(f):
    try:
        return float(f)
    except:
        return 0


FIPS = "36"
STATE_PREFIX = "ny" # ca: 6, co: 8, mt: 30, ny: 36, wi: 55

client = FIADB(verbose=True)

acres_per_county = client.fullreport.get(
    reptype="State",
    snum="Area of sampled land and water, in acres",
    wc=FIPS + "2018",
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
    wc=FIPS + "2018",
    pselected="Species",  # For more grouping, less descriptive names: "Species group"
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

for page in data:
    title = "All" if page == "Page total" else page.replace("/", " or ")
    output_matrix = [["FIPS", "PER_COUNTY"]]
    for county in acres:
        try:
            output_matrix.append([county, data[page][county] / acres[county]])
        except KeyError:
            output_matrix.append([county, 0])

    with open(
        "data/" + STATE_PREFIX + "_" + title + ".csv", "w+", newline=""
    ) as output_csv:
        csvWriter = csv.writer(output_csv, delimiter=",")
        csvWriter.writerows(output_matrix)
