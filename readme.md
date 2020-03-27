## Documentation & Links
> https://apps.fs.usda.gov/fia/datamart/images/datamart_api_tutorials.html
General documentation

> https://apps.fs.usda.gov/fia/datamart/images/Evalidator_variable_library.html
List of variables

> https://apps.fs.usda.gov/fia/datamart/images/Evalidator_pop_estimates.html
List of population estimates

> https://www.fia.fs.fed.us/library/database-documentation/
Documentation PDFs, including information at the table level

## fullReport Example



## evalgrp Example
[Web Example: All evalGrp for Alabama (StateCD = 1)](https://apps.fs.usda.gov/Evalidator/rest/Evalidator/evalgrp?schemaName=FS_FIADB&whereClause=STATECD+IN+(1)&mostRecent=N)

```python
# Most recent evalGrps for Minnesota, Wisconsin
client.evalgrp.get(whereClause="STATECD IN (55, 27)")
> [272018, 552018]
```

## statecdLonLatRad Example
[Web Example: all state codes within 600mi of Minneapolis, MN](https://apps.fs.usda.gov/Evalidator/rest/Evalidator/statecdLonLatRad?lon=-93&lat=45&rad=600&schemaName=FS_FIA_SPATIAL) (*Note:* the FIADB table returns some codes as strings and others as numbers.)

```python
# State codes within 100mi of Minneapolis, MN
str(client.statecdLonLatRad.get(lat=45, lon=93, rad=100))
> [55, 27]
```

## refTable Example
[Web Example: A list of all species in the database.](https://apps.fs.usda.gov/Evalidator/rest/Evalidator/refTable?colList=common_name,%20genus,%20species&tableName=REF_SPECIES&whereStr=upper(common_name)%20like%20%27%%%27&outputFormat=HTML)

```python
# List all unique entries with "walnut" in the common name
walnuts = client.refTable.get(tableName="REF_SPECIES", colList="common_name, genus, species", whereStr="upper(common_name) LIKE '%WALNUT%'\r\n")
"\r\n".join(["%s | *%s %s*" % (e['COMMON_NAME'], e['GENUS'], e['SPECIES']) for e in walnuts])
```

Common Name | Species
-------------- | -------------
West Indian walnut | *Juglans jamaicensis*
English walnut | *Juglans regia*
Indian walnut | *Aleurites moluccana*
walnut spp. | *Juglans spp.*
black walnut | *Juglans nigra*
northern California black walnut | *Juglans hindsii*
southern California black walnut | *Juglans californica*
Texas walnut | *Juglans microcarpa*
Arizona walnut | *Juglans major*