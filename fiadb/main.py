import warnings
import re


def new_session(*args, **kwargs):
    import requests
    return requests.session(*args, **kwargs)


class APIKeyError(Exception):
    """ Invalid API key
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class APIException(Exception):
    pass


class Client(object):
    
    def __init__(self, session=None, retries=3):
        self.session = session or new_session()
        self.retries = retries


class FIADBfullreport(Client):

    def __init__(self, session=None):
        Client.__init__(self)
        self.endpoint_url = 'https://apps.fs.usda.gov/Evalidator/rest/Evalidator/refTable'

    def tables(self, *args, **kwargs):
        return "TODO"

    def get(self, *args, **kwargs):
        return "TODO"


class FIADBevalgrp(Client):
    """ To identify which evaluation groups are in the database """

    def __init__(self, session=None):
        Client.__init__(self)
        self.endpoint_url = 'https://apps.fs.usda.gov/Evalidator/rest/Evalidator/evalgrp'
        self.available_cols = FIADBrefTable().columns(tableName="POP_EVAL_GRP")

    def get(self, whereClause="", mostRecent="Y", **kwargs):
        return (self.query(whereClause, mostRecent, **kwargs))

    def query(self, whereClause="", mostRecent="Y", **kwargs):

        url = self.endpoint_url

        params = {
            'schemaName': "FS_FIADB",
            'whereClause': whereClause, # Usually blank but user can use any fields in the `POP_EVAL_GRP` table to limit the number of rows
            'mostRecent': mostRecent,   # If "Y" then only the most recent inventories (based on `DATAMART_MOST_RECENT_INV`) will be returned
        }

        resp = self.session.get(url, params=params)
        print(resp.url) # For troubleshooting

        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError as ex:
                raise ex

            if data['listOfEvalGroups'] == "":
                return ["Empty evalGrp query results"]
            return data['listOfEvalGroups']['evalGrp']

        elif resp.status_code == 204:
            return []

        else:
            raise APIException("An error occured.")



class FIADBstatecdLonLatRad(Client):

    def __init__(self, session=None):
        Client.__init__(self)
        self.endpoint_url = 'https://apps.fs.usda.gov/Evalidator/rest/Evalidator/statecdLonLatRad'


    def get(self, lon, lat, rad=0, **kwargs):
        return (self.query(lon, lat, rad, **kwargs))


    def query(self, lon, lat, rad=0, **kwargs):

        url = self.endpoint_url

        params = {
            'lon': -abs(lon), # NAD83
            'lat': lat,       # NAD83; Note: all longitude values should be negative
            'rad': rad,
            'schemaName': "FS_FIA_SPATIAL"
        }

        resp = self.session.get(url, params=params)
        # print(resp.url) # For troubleshooting

        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError as ex:
                raise ex

            if data['listOfStatecds'] == "":
                return ["Empty stateLonLatRad query results"]
            return data['listOfStatecds']['statecd']

        elif resp.status_code == 204:
            return []

        else:
            raise APIException("An error occured.")



class FIADBrefTable(Client):

    def __init__(self, session=None):
        Client.__init__(self)
        self.endpoint_url = 'https://apps.fs.usda.gov/Evalidator/rest/Evalidator/refTable'

    def tables(self, *args, **kwargs):
        # For now, it looks like we need to download this list in HTML and parse it.
        resp = self.session.get("https://apps.fs.usda.gov/fia/datamart/CSV/datamart_csv.html")

        if resp.status_code == 200:
            csvs = re.findall(r'"(\w+\.csv)"', resp.text)
            return (csvs)

        else:
            raise APIException("An unknown error occured while attempting to access a list of available tables.")


    def columns(self, tableName, *args, **kwargs):
        result = self.query(tableName, colList="*", whereStr="ROWNUM=1")
        return list(result.keys())


    def get(self, **kwargs):
        return (self.query(**kwargs))


    def query(self, tableName, colList="*", whereStr="1=1", **kwargs):

        url = self.endpoint_url

        params = {
            'colList': colList, # use * for all
            'tableName': tableName,
            'whereStr': whereStr,
            'outputFormat': "JSON"
        }

        resp = self.session.get(url, params=params)
        # print(resp.url) # For troubleshooting

        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError as ex:
                if '<title>Invalid Key</title>' in resp.text:
                    raise APIKeyError('Invalid key')
                else:
                    raise ex

            if data['FIADB_SQL_Output'] == "":
                return ["Empty query results"]
            return data['FIADB_SQL_Output']['record']

        elif resp.status_code == 204:
            return []

        elif resp.status_code == 500:
            if 'invalid identifier' in resp.text:
                raise APIException("Error " + str(resp.status_code) +": invalid identifier")
            if 'invalid relational operator' in resp.text:
                raise APIException("Error " + str(resp.status_code) +": invalid relational operator: use '=', '!=', 'LIKE', 'NOT LIKE', etc.")
            if 'missing expression' in resp.text:
                raise APIException("Error " + str(resp.status_code) +": missing expression (did you use '==' when you meant '='?)")
            else:
                raise APIException("Error " + str(resp.status_code) +": Unknown error occured.")

        else:
            raise APIException("An unknown error occured.")



class FIADB(object):

    def __init__(self, year=None, session=None):

        if not session:
            session = new_session()

        self.session = session
        self.session.headers.update({
            'User-Agent': ('python-usda-fs-fiadb')
        })

        self.fullreport = FIADBfullreport(session)
        self.statecdLonLatRad = FIADBstatecdLonLatRad(session)
        self.refTable = FIADBrefTable(session)
        self.evalgrp = FIADBevalgrp(session)

