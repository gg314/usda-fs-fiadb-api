## Python USDA Forest Inventory and Analysis Database API Wrapper

This is a fairly simple wrapper to the APIs available from the US Forest Service's <abbr title="Forest Inventory and Analysis Database">FIADB</abbr>.

## Documentation & Links

[General FIADB API "documentation"](https://apps.fs.usda.gov/fia/datamart/images/datamart_api_tutorials.html)

[List of `fullReport` variables](https://apps.fs.usda.gov/fia/datamart/images/Evalidator_variable_library.html)

[List of `fullReport` population estimates](https://apps.fs.usda.gov/fia/datamart/images/Evalidator_pop_estimates.html) or use `FIADB.fullreport.list_attributes()`

[Table documentation PDFs](https://www.fia.fs.fed.us/library/database-documentation/)

## Usage

```python
from fiadb import FIADB

client = FIADB()               # or:
client = FIADB(verbose = True) # print HTTP request urls for each query
```

### fullreport Example

Valid fullReport queries can be very difficult to write and parse without testing first on the USDA's Java-based [Evalidator](https://apps.fs.usda.gov/Evalidator/evalidator.jsp).

[Web example: Get all species in Wisconsin grouped by county](<https://apps.fs.usda.gov/Evalidator/rest/Evalidator/fullreport?reptype=State&lat=0&lon=0&radius=0&snum=Number%20of%20live%20trees%20(at%20least%201%20inch%20d.b.h./d.r.c.),%20in%20trees,%20on%20forest%20land&sdenom=No%20denominator%20-%20just%20produce%20estimates&wc=552018&pselected=Species%20group&rselected=County%20code%20and%20name&cselected=All%20live%20stocking&ptime=Current&rtime=Current&ctime=Current&wf=&wnum=&wnumdenom=&FIAorRPA=FIADEF&outputFormat=HTML&estOnly=Y&schemaName=FS_FIADB.>)

[Web example: Get acres per country](https://apps.fs.usda.gov/Evalidator/rest/Evalidator/fullreport?reptype=State&lat=0&lon=0&radius=0&snum=Area%20of%20sampled%20land%20and%20water,%20in%20acres&sdenom=No%20denominator%20-%20just%20produce%20estimates&wc=552018&pselected=None&rselected=County%20code%20and%20name&cselected=EVALID&ptime=Current&rtime=Current&ctime=Current&wf=&wnum=&wnumdenom=&FIAorRPA=FIADEF&outputFormat=HTML&estOnly=Y&schemaName=FS_FIADB.)

```python
# Find total number of softwood and hardwood trees by Wisconsin county
trees = client.fullreport.get(
    reptype="State",
    snum="Number of live trees (at least 1 inch d.b.h./d.r.c.), in trees, on forest land",
    wc=552018,
    pselected="None",
    rselected="County code and name",
    cselected="Species group - Major"
)
```

### evalgrp Example
```python
# Most recent evalGrps for Minnesota, Wisconsin
client.evalgrp.get(whereClause="STATECD IN (55, 27)")
> [272018, 552018]
```

### statecdlonlatrad Example
```python
# State codes within 100mi of Minneapolis, MN
client.statecdlonlatrad.get(lat=45, lon=93, rad=100)
> [55, 27]
```

### reftable Example

[Web Example: A list of all species in the database.](<https://apps.fs.usda.gov/Evalidator/rest/Evalidator/refTable?colList=common_name,%20genus,%20species&tableName=REF_SPECIES&whereStr=upper(common_name)%20like%20%27%%%27&outputFormat=HTML>)

```python
# List all unique entries with "walnut" in the common name
walnuts = client.reftable.get(
    tableName="REF_SPECIES",
    colList="common_name, genus, species",
    whereStr="upper(common_name) LIKE '%WALNUT%'\r\n"
)
"\r\n".join(["%s | *%s %s*" % (e['COMMON_NAME'], e['GENUS'], e['SPECIES']) for e in walnuts])
```

| Common Name                      | Species               |
| -------------------------------- | --------------------- |
| West Indian walnut               | _Juglans jamaicensis_ |
| English walnut                   | _Juglans regia_       |
| Indian walnut                    | _Aleurites moluccana_ |
| walnut spp.                      | _Juglans spp._        |
| black walnut                     | _Juglans nigra_       |
| northern California black walnut | _Juglans hindsii_     |
| southern California black walnut | _Juglans californica_ |
| Texas walnut                     | _Juglans microcarpa_  |
| Arizona walnut                   | _Juglans major_       |
