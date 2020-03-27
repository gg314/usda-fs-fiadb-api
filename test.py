from fiadb import FIADB

# from us import states # future: fips

client = FIADB()


test = client.reftable.get("POP_")
print(test)
quit()

# results = client.fullreport.get(reptype="Circle", lat="45", lon="-93", radius="50", snum="Area of forest land, in acres", sdenom="No denominator - just produce estimates", wc=272018, pselected="None", rselected="Stand-size class", cselected="Ownership group - Major")
areas = client.fullreport.get(
    reptype="State",
    snum="Area of sampled land and water, in acres",
    sdenom="No denominator - just produce estimates",
    wc=552018,
    pselected="None",
    rselected="County code and name",
    cselected="EVALID",
)
areas = areas["row"]

trees = client.fullreport.get(
    reptype="State",
    snum="Number of live trees (at least 1 inch d.b.h./d.r.c.), in trees, on forest land",
    sdenom="No denominator - just produce estimates",
    wc=552018,
    pselected="None",
    rselected="County code and name",
    cselected="Species group - Major",
)
trees = trees["row"]

tree_counts_by_county = {}
for c in trees:
    tree_counts_by_county[c["content"]] = (
        int(c["column"][0]["cellValueNumerator"]),
        int(c["column"][1]["cellValueNumerator"]),
        int(c["column"][2]["cellValueNumerator"]),
    )

acres_by_county = {}
for z in areas:
    acres_by_county[z["content"]] = int(z["column"][0]["cellValueNumerator"])

tree_density_by_county = {}
for county in acres_by_county.keys():
    try:
        fips = int(county[2:5])
    except:
        fips = -1

    if fips > 0:
        tree_density_by_county[fips] = (
            int(tree_counts_by_county[county][0] / acres_by_county[county]),
            int(tree_counts_by_county[county][1] / acres_by_county[county]),
            int(tree_counts_by_county[county][2] / acres_by_county[county]),
        )


for k in tree_density_by_county:
    print(
        "%s, %d, %d, %d"
        % (
            k,
            tree_density_by_county[k][0],
            tree_density_by_county[k][1],
            tree_density_by_county[k][2],
        )
    )


quit()

print(
    "Most recent EvalGrps for Minnesota, Wisconsin: "
    + str(client.evalgrp.get(whereClause="XSTATECD IN (55, 27)"))
    + "\r\n"
)

quit()


quit()

print("Found " + str(len(client.reftable.tables())) + " available FIADB tables.\r\n")

walnuts = client.reftable.get(
    tableName="REF_SPECIES",
    colList="common_name, genus, species",
    whereStr="upper(common_name) LIKE '%WALNUT%'\r\n",
)
print(
    "Found %d species of walnut: " % len(walnuts)
    + "\r\n".join(
        ["%s | *%s %s*" % (e["COMMON_NAME"], e["GENUS"], e["SPECIES"]) for e in walnuts]
    )
    + "\r\n"
)

print(
    "Columns in `TREE`: "
    + ", ".join(client.reftable.columns(tableName="TREE"))
    + "\r\n"
)

print(
    "Columns in `POP_EVAL_GRP`: "
    + ", ".join(client.reftable.columns(tableName="POP_EVAL_GRP"))
    + "\r\n"
)

print(
    "State codes within 100mi of Minneapolis, MN: "
    + str(client.statecdlonlatrad.get(lat=45, lon=93, rad=100))
    + "\r\n"
)
