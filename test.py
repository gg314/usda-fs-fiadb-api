from fiadb import FIADB
# from us import states # future: fips

client = FIADB()

print("Found " + str(len(client.refTable.tables())) + " available tables.\r\n")

walnuts = client.refTable.get(tableName="REF_SPECIES", colList="common_name, genus, species", whereStr="upper(common_name) LIKE '%WALNUT%'\r\n")
print("Found %d species of walnut: " % len(walnuts) + "\r\n".join(["%s | *%s %s*" % (e['COMMON_NAME'], e['GENUS'], e['SPECIES']) for e in walnuts]) + "\r\n")

print("Columns in `TREE`: " + ", ".join(client.refTable.columns(tableName="TREE")) + "\r\n")

print("Columns in `REF_SPECIES`: " + ", ".join(client.refTable.columns(tableName="REF_SPECIES")) + "\r\n")