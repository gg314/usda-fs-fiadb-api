## Python USDA Forest Inventory and Analysis Database API Wrapper
This is a fairly simple wrapper to the APIs available from the U.S. Forest Service's <abbr title="Forest Inventory and Analysis Database">FIADB</abbr>.

## Documentation & Links
[General FIADB API "documentation"](https://apps.fs.usda.gov/fia/datamart/images/datamart_api_tutorials.html)

[List of `fullReport` variables](https://apps.fs.usda.gov/fia/datamart/images/Evalidator_variable_library.html)

[List of `fullReport` population estimates](https://apps.fs.usda.gov/fia/datamart/images/Evalidator_pop_estimates.html)

[Documentation PDFs, including information at the table level](https://www.fia.fs.fed.us/library/database-documentation/)

## fullReport Example
FullReport queries can be very difficult to write and parse without testing first on the USDA's Java-based [Evalidator](https://apps.fs.usda.gov/Evalidator/evalidator.jsp).

[Web example: Get all species in Wisconsin grouped by county](https://apps.fs.usda.gov/Evalidator/rest/Evalidator/fullreport?reptype=State&lat=0&lon=0&radius=0&snum=Number%20of%20live%20trees%20(at%20least%201%20inch%20d.b.h./d.r.c.),%20in%20trees,%20on%20forest%20land&sdenom=No%20denominator%20-%20just%20produce%20estimates&wc=552018&pselected=Species%20group&rselected=County%20code%20and%20name&cselected=All%20live%20stocking&ptime=Current&rtime=Current&ctime=Current&wf=&wnum=&wnumdenom=&FIAorRPA=FIADEF&outputFormat=HTML&estOnly=Y&schemaName=FS_FIADB.)

[Web example: Get acres per country](https://apps.fs.usda.gov/Evalidator/rest/Evalidator/fullreport?reptype=State&lat=0&lon=0&radius=0&snum=Area%20of%20sampled%20land%20and%20water,%20in%20acres&sdenom=No%20denominator%20-%20just%20produce%20estimates&wc=552018&pselected=None&rselected=County%20code%20and%20name&cselected=EVALID&ptime=Current&rtime=Current&ctime=Current&wf=&wnum=&wnumdenom=&FIAorRPA=FIADEF&outputFormat=HTML&estOnly=Y&schemaName=FS_FIADB.)

```python
# Find total number of softwood and hardwood trees by Wisconsin county
trees = client.fullreport.get(reptype="State", lat="0", lon="0", radius="0", snum="Number of live trees (at least 1 inch d.b.h./d.r.c.), in trees, on forest land", sdenom="No denominator - just produce estimates", wc=552018, pselected="None", rselected="County code and name", cselected="Species group - Major")
```

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