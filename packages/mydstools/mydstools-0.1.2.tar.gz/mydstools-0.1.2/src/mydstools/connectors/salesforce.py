from simple_salesforce import Salesforce
import pandas as pd
import requests
from io import StringIO
import os
from ..cleaning import clean_col_names


class SalesforceConn:
    def __init__(self, user, password, token):
        self.sf_instance = 'https://rydoo.lightning.force.com/'
        self.sf = Salesforce(user, password, token)

    def get_report(self, reportid):
        export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
        sfUrl = self.sf_instance + reportid + export
        response = requests.post(
            sfUrl,
            headers=self.sf.headers,
            cookies={'sid': self.sf.session_id}
            )
        
        download_report = response.content.decode('utf-8')

        df = pd.read_csv(StringIO(download_report))
        df.columns = clean_col_names(df.columns)
        return df

    def object_names(self):
        objects = self.sf.restful('sobjects')
        return [object['name'] for object in objects['sobjects']]
    
    def query(self, query):
        return self.sf.query_all(query)