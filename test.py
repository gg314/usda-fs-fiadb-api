from fiadb import FIADB
# from us import states # future: fips

client = FIADB()


#results = client.fullreport.get(reptype="Circle", lat="45", lon="-93", radius="50", snum="Area of forest land, in acres", sdenom="No denominator - just produce estimates", wc=272018, pselected="None", rselected="Stand-size class", cselected="Ownership group - Major")
areas = client.fullreport.get(reptype="State", snum="Area of sampled land and water, in acres", sdenom="No denominator - just produce estimates", wc=552018, pselected="None", rselected="County code and name", cselected="EVALID")
areas = areas['row']

trees = client.fullreport.get(reptype="State", snum="Number of live trees (at least 1 inch d.b.h./d.r.c.), in trees, on forest land", sdenom="No denominator - just produce estimates", wc=552018, pselected="None", rselected="County code and name", cselected="Species group - Major")
trees = trees['row']

treeCountsByCounty = {}
for c in trees:
  treeCountsByCounty[c["content"]] = (int(c["column"][0]["cellValueNumerator"]), int(c["column"][1]["cellValueNumerator"]), int(c["column"][2]["cellValueNumerator"]))

areaByCounty = {}
for z in areas:
  areaByCounty[z["content"]] = int(z["column"][0]["cellValueNumerator"])

densityByCounty = {}
for county in areaByCounty.keys():
  try:
    fips = int(county[2:5])
  except:
    fips = -1
  
  if fips > 0:
    densityByCounty[fips] = (int(treeCountsByCounty[county][0] / areaByCounty[county]), int(treeCountsByCounty[county][1] / areaByCounty[county]), int(treeCountsByCounty[county][2] / areaByCounty[county]))


for k in densityByCounty:
  print("%s, %d, %d, %d" % (k, densityByCounty[k][0], densityByCounty[k][1], densityByCounty[k][2] ) )


# results = client.refTable.get(tableName="POP_EVAL_GRP", colList="eval_grp, eval_grp_descr")
# print("\r\n".join([ "%s (%s)" % (r['EVAL_GRP'], r['EVAL_GRP_DESCR']) for r in results ]))

quit()

print("Most recent EvalGrps for Minnesota, Wisconsin: " + str(client.evalgrp.get(whereClause="XSTATECD IN (55, 27)")) + "\r\n")

quit()





quit()

print("Found " + str(len(client.refTable.tables())) + " available FIADB tables.\r\n")

walnuts = client.refTable.get(tableName="REF_SPECIES", colList="common_name, genus, species", whereStr="upper(common_name) LIKE '%WALNUT%'\r\n")
print("Found %d species of walnut: " % len(walnuts) + "\r\n".join(["%s | *%s %s*" % (e['COMMON_NAME'], e['GENUS'], e['SPECIES']) for e in walnuts]) + "\r\n")

print("Columns in `TREE`: " + ", ".join(client.refTable.columns(tableName="TREE")) + "\r\n")

print("Columns in `POP_EVAL_GRP`: " + ", ".join(client.refTable.columns(tableName="POP_EVAL_GRP")) + "\r\n")

print("State codes within 100mi of Minneapolis, MN: " + str(client.statecdLonLatRad.get(lat=45, lon=93, rad=100)) + "\r\n")

