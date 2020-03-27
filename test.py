from fiadb import FIADB

# from us import states # future: fips

client = FIADB(verbose=False)


# State codes within 100mi of Minneapolis, MN
states_near_MN = client.statecdlonlatrad.get(lat=45, lon=-93.0, rad=100)
print(states_near_MN)


latest_MN_WI_data = client.evalgrp.get(whereClause="STATECD IN (55, 27)")
print(latest_MN_WI_data)


walnuts = client.reftable.get(
    tableName="REF_SPECIES",
    colList="common_name, genus, species",
    whereStr="upper(common_name) LIKE '%WALNUT%'\r\n",
)
print(
    "\r\n".join(
        ["%35s | %s %s" % (e["COMMON_NAME"], e["GENUS"], e["SPECIES"]) for e in walnuts]
    )
)


# results = client.fullreport.get(reptype="Circle", lat="45", lon="-93", radius="50", snum="Area of forest land, in acres", sdenom="No denominator - just produce estimates", wc=272018, pselected="None", rselected="Stand-size class", cselected="Ownership group - Major")

areas = client.fullreport.get(
    reptype="State",
    snum="Area of sampled land and water, in acres",
    wc=552018,
    pselected="None",
    rselected="County code and name",
    cselected="EVALID",
)["row"]
acres_by_county = {
    a["content"]: int(a["column"][0]["cellValueNumerator"]) for a in areas
}

trees = client.fullreport.get(
    reptype="State",
    snum="Number of live trees (at least 1 inch d.b.h./d.r.c.), in trees, on forest land",
    wc=552018,
    pselected="None",
    rselected="County code and name",
    cselected="Species group - Major",
)["row"]

tree_counts_by_county = {
    t["content"]: [int(t["column"][i]["cellValueNumerator"]) for i in range(3)]
    for t in trees
}

tree_density_by_county = {}
for county in acres_by_county.keys():
    try:
        fips = int(county[2:5])
        tree_density_by_county[fips] = [
            int(tree_counts_by_county[county][i] / acres_by_county[county])
            for i in range(3)
        ]

    except ValueError:
        pass

print(tree_density_by_county)


quit()

print("Found " + str(len(client.reftable.tables())) + " available FIADB tables.\r\n")


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
