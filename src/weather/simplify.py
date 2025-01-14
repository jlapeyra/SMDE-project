import pandas as pd
from typing import Iterable
import json

def average(values:Iterable):
    valid = [x for x in values if x is not None]
    if valid == []:
        return None
    return sum(valid)/len(valid)


table = []

with open('data/meteocat/data.dat') as file:
    for line in file:
        date, data = line.strip('\n').split(';', 1)
        year, month, day = map(int, date.split('-'))
        data:dict = json.loads(data)
        temperature = data.get('temperatura-avg')
        humidity = data.get('humitat-avg')
        #temperature = average(data.get('temperatura', []))
        #humidity = average(data.get('humitat', []))
        wind = average(data.get('velocitatVent', []))
        table.append([year,month,day, temperature,humidity,wind])


import utils
pd.DataFrame(table, columns=['Year', 'Month', 'Day', 'Temperature', 'Humidity', 'Wind'])\
    .map(utils.float_formatter(3))\
    .to_csv('data/meteocat/simplified.csv', index=False)
