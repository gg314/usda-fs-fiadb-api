from fiadb import FIADB
# from us import states # future: fips

client = FIADB()

print("Found " + str(len(client.refTable.tables())) + " available tables.\r\n")

walnuts = client.refTable.get(tableName="REF_SPECIES", colList="common_name, genus, species", whereStr="upper(common_name) LIKE '%WALNUT%'\r\n")
print("Found %d species of walnut: " % len(walnuts) + "\r\n".join(["%s | *%s %s*" % (e['COMMON_NAME'], e['GENUS'], e['SPECIES']) for e in walnuts]) + "\r\n")

print("Columns in `TREE`: " + ", ".join(client.refTable.columns(tableName="TREE")) + "\r\n")

print("Columns in `POP_EVAL_GRP`: " + ", ".join(client.refTable.columns(tableName="POP_EVAL_GRP")) + "\r\n")

print("State codes within 100mi of Minneapolis, MN: " + str(client.statecdLonLatRad.get(lat=45, lon=93, rad=100)) + "\r\n")

print("Most recent EvalGrps for Minnesota, Wisconsin: " + str(client.evalgrp.get(whereClause="STATECD IN (55, 27)")) + "\r\n")