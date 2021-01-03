import pandas_datareader as web
from pandas import DataFrame
from pandas import concat
import math
import numpy as np
import pandas as pd
import warnings
from pandas import json_normalize
import requests
import datetime as dt
from datetime import timedelta
from datetime import datetime
import time
import sys
import requests
import json
import os
print("Setup Complete")
starting_time=time.time()

#10010: Wind p48
#84: SolarPV p48
#10027: Total Demand p48 ,'510','514'
#472:Hydro generation availability
#474: Nuclear generation availability
#475: Fossil hard generaiton availability
#477: CCGT generation availability
#10001: Total power generation availability
#552: Powernext France power price real
#2584: OMEI Spain power price real

ree_id_list=['472','474','475','477','10001']

cookies_ree = {
}

headers_ree = {
    'Accept': 'application/json; application/vnd.esios-api-v1+json',
    'Content-Type': 'application/json',
    'Host': 'api.esios.ree.es',
    'Authorization': 'Token token="PLEASE INSERT YOUR OWN PERSONAL API_KEY"',
}

params_ree = (
    ('start_date', start_ree.isoformat()),
    ('end_date', end_ree.isoformat()),
)

appended_ree=[]
for x in ree_id_list:
    url='https://api.esios.ree.es/indicators/'+x
    response=requests.get(url, headers=headers_ree, params=params_ree, cookies=cookies_ree)
    response=response.json()
    #response=json.loads(response.txt)
    ree_data=pd.json_normalize(response)
    ree_id=ree_data['indicator.id'].astype(str)
    ree_id=ree_id[0]
    ree_data=ree_data['indicator.values'][0]
    ree_data=pd.json_normalize(ree_data)
    ree_data=ree_data.drop(['datetime_utc','tz_time','geo_id','geo_name'],axis=1)
    ree_data=ree_data.set_index('datetime')
    ree_data.index=pd.to_datetime(ree_data.index, format='%Y-%m-%d %H:%M',utc=False)
    #ree_data.index=ree_data.index.strftime('%d/%m/%Y %H:%M')
    ree_data['date']=ree_data.index
    ree_data=ree_data.groupby(ree_data['date']).mean()
    ree_data.columns=[ree_id]
    appended_ree.append(ree_data)

appended_ree=pd.concat(appended_ree,axis=1,sort=True)
ree_generation_capacity=appended_ree
ree_generation_capacity.index=pd.to_datetime(ree_generation_capacity.index, format='%Y-%m-%d %H:%M:%S',utc=True)
print(ree_generation_capacity)
print('PROCESS TOOK |%s| SECONDS TO BE COMPLETED' % (time.time()-starting_time))


