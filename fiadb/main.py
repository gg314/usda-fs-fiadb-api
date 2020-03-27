import warnings
import re


def new_session(*args, **kwargs):
    import requests
    return requests.session(*args, **kwargs)


def test_param(param, set):
    if param in set:
        return param
    else:
        print('o no')
        raise APIException("API Input Error: '" + str(param) + "' should be one of " + str(set))

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
        self.endpoint_url = 'https://apps.fs.usda.gov/Evalidator/rest/Evalidator/fullreport'


    def list_attributes(self, *args, **kwargs):
        """ 
        return a list of (NUMBER, DESCRIPTION, TIMBERLAND_ONLY) of attributes that can be used in fullReport's snum, etc.
         - TIMBERLAND displays whether the attribute is limited to timberland.
        """
        try:
            return self.attributes
        except AttributeError:
            query = FIADBrefTable().get(tableName="REF_POP_ATTRIBUTE", colList="ATTRIBUTE_NBR, ATTRIBUTE_DESCR, TIMBERLAND")
            self.attributes = sorted([(p['ATTRIBUTE_NBR'], p['ATTRIBUTE_DESCR'], p['TIMBERLAND']) for p in query], key=lambda tup: tup[0])
            return self.attributes


    def list_evalgrps(self, *args, **kwargs):
        """ 
        return a list of (EVAL_GRP, EVAL_GRP_DESCR, STATECD) of eval_grps that can be used in fullReport's wc.
        sorted by earliest to latest, for some reason.
        """
        try:
            return self.eval_grps
        except AttributeError:
            query = FIADBrefTable().get(tableName="POP_EVAL_GRP", colList="EVAL_GRP, EVAL_GRP_DESCR, STATECD")
            self.eval_grps = sorted([(p['EVAL_GRP'], p['EVAL_GRP_DESCR'], p['STATECD']) for p in query], key=lambda tup: str(tup[0])[-4:])
            return self.eval_grps

    def list_vars(self, type="*", *args, **kwargs):
        """ 
        return a list of () (used in fullReport's pselected, rselected, cselected).
        sorted by earliest to latest, for some reason.
        """
        try:
            all_vars = self.variables
        except AttributeError:
            query = FIADBrefTable().get(tableName="POP_EVAL_GRP", colList="EVAL_GRP, EVAL_GRP_DESCR, STATECD")
            self.variables = sorted([(p['EVAL_GRP'], p['EVAL_GRP_DESCR'], p['STATECD']) for p in query], key=lambda tup: str(tup[0])[-4:])
            all_vars = self.variables
        
        return all_vars


    def get(self, **kwargs):
        return (self.query(**kwargs))

    def query(self,
              reptype="State",
              lat=0,
              lon=0,
              radius=0,
              snum="",
              sdenom="No denominator - just produce estimates",
              wc="",
              pselected="",
              rselected="",
              cselected="",
              ptime="Current",
              rtime="Current",
              ctime="Current",
              wf="",
              wnum="",
              wnumdenom="",
              FIAorRPA="FIADEF",
              estOnly="Y",
              r1="",
              c1="",
              **kwargs):

        url = self.endpoint_url
        time_opts = ["Accounting", "Previous", "Current", "Previous if available else current", "Current if available else previous"]
        params = {
            'reptype': test_param(reptype, ["Circle", "State"]),
            'lat': lat,       # NAD83; Note: all longitude values should be negative
            'lon': lon, # NAD83
            'radius': radius, # if using repType="Circle", in [miles]
            'snum': snum,     # Numerator: See values of self.list_attributes()
            'sdenom': sdenom, # Denominator: If not performing a ratio estimate then enter 0, "No denominator -just produce estimate." For ratio estimates see values of self.list_attributes().
            'wc': wc,         # which dataset? See values of self.list_evalgrps(). When more than one evaluation group is selected, evaluation group numbers are comma-separated. Use evalGrp API to find group by state.
            'pselected': pselected, # See label_var variable in variable_library online table where page_list='Y'.
            'rselected': rselected, # See label_var variable in variable_library online table where row_list='Y'.
            'cselected': cselected, # See label_var variable in variable_library online table where col_list='Y'
            'ptime': test_param(ptime, time_opts),
            'rtime': test_param(rtime, time_opts),
            'ctime': test_param(ctime, time_opts),
            'wf': wf,                # SQL clause filter used for non-ratio estimates
            'wnum': wnum,            # SQL clause filter, applied only to numerator in a ratio estimate
            'wnumdenom': wnumdenom,  # SQL clause filter, applied to numerator and denominator in ratio estimate
            'FIAorRPA': test_param(FIAorRPA, ["FIADEF", "RPADEF"]),
            'outputFormat': "JSON",
            'estOnly': test_param(estOnly, ["Y", "N"]),
            'schemaName': "FS_FIADB.",
            'r1': r1,
            'c1': c1,
        }

        resp = self.session.get(url, params=params)
        print(resp.url) # For troubleshooting

        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError as ex:
                raise ex

            if data['EVALIDatorOutput'] == "":
               return ["Empty evalGrp query results"]
            return data['EVALIDatorOutput']

        elif resp.status_code == 204:
            return []

        else:
            raise APIException("An error occured.")



class FIADBevalgrp(Client):
    """ To identify which evaluation groups are in the database """

    def __init__(self, session=None):
        Client.__init__(self)
        self.endpoint_url = 'https://apps.fs.usda.gov/Evalidator/rest/Evalidator/evalgrp'


    def columns(self, *args, **kwargs):
        """ 
        return a list of columns from `POP_EVAL_GRP` that can be used in a whereClause.
        """
        try:
            return self.available_cols
        except AttributeError:
            self.available_cols = FIADBrefTable().columns(tableName="POP_EVAL_GRP")
            return self.available_cols


    def get(self, whereClause="", mostRecent="Y", **kwargs):
        return (self.query(whereClause, mostRecent, **kwargs))

    def query(self, whereClause="", mostRecent="Y", **kwargs):

        url = self.endpoint_url

        params = {
            'schemaName': "FS_FIADB",
            'whereClause': whereClause, # "Usually blank but can use any fields in the `POP_EVAL_GRP` table to limit the number of rows"
            'mostRecent': test_param(mostRecent, ["Y", "N"]),   # If "Y" then only the most recent inventories (based on `DATAMART_MOST_RECENT_INV`) will be returned
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
            raise APIException("An error occured. For a list of available POP_EVAL_GRP fields to use in whereClause, evaluate `self.evalgrp.available_cols`")



class FIADBstatecdLonLatRad(Client):

    def __init__(self, session=None):
        Client.__init__(self)
        self.endpoint_url = 'https://apps.fs.usda.gov/Evalidator/rest/Evalidator/statecdLonLatRad'


    def get(self, lon, lat, rad=0, **kwargs):
        return (self.query(lon, lat, rad, **kwargs))


    def query(self, lon, lat, rad=0, **kwargs):

        url = self.endpoint_url

        params = {
            'lon': -abs(lon), # NAD83; Note: all longitude values should be negative
            'lat': lat,       # NAD83
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


    def get(self, tableName, colList="*", whereStr="1=1", **kwargs):
        return (self.query(tableName, colList, whereStr, **kwargs))


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

