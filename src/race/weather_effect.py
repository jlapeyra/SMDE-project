import numpy as np
import pandas as pd
from math import prod

class Weather:
    def __init__(self, temp, humi, wind):
        self.data = (('temp', temp), ('humi', humi), ('wind', wind))

    def effect(self, *attr):
        return prod(WEATHER_EFFECT[*attr, lev, prop] for prop,lev in self.data)
    

def __load_weather_effect():
    df = pd.read_csv('data/effect.csv')
    dict_data = {}
    for _,row in df.iterrows():
        dict_data[row['gender'], row['level'], row['prop']] = row['value']
    return {
        (g, l, p) : dict_data[g,l,p]/dict_data[g,'me',p]
        for g, l, p in dict_data.keys()
    }

WEATHER_EFFECT = __load_weather_effect()

#####################################

def __original_weather():
    raw_og = {}
    # Sources:
    #    https://www.baa.org/races/boston-marathon/plan/marathon-dates
    #    https://www.timeanddate.com/weather/usa/boston/historic (2015-04-20, 2016-04-18, 2017-04-17)
    raw_og[2015, 'temp'] = 6,5,5,5,5,5,6,6,6,6,7,7,6,7,7,7,7,7,7,8,10,11,10,11
    raw_og[2015, 'humi'] = 82,80,86,89,93,93,89,89,89,92,82,82,89,89,89,90,96,96,100,97,100,96,100,100
    raw_og[2015, 'wind'] = 11,9,9,15,15,13,13,22,28,28,28,35,30,26,32,28,22,22,22,24,15,30,26,24
    raw_og[2016, 'temp'] = 8,8,7,7,7,8,9,13,16,19,17,15,14,12,11,11,11,10,9,9,8,8,8,8,
    raw_og[2016, 'humi'] = 59,68,68,63,63,56,48,40,34,27,38,41,42,55,57,57,56,54,57,56,66,66,71,66,
    raw_og[2016, 'wind'] = 11,11,9,9,6,11,7,7,13,22,32,28,22,17,19,19,22,19,19,13,11,7,
    raw_og[2017, 'temp'] = 20,19,19,19,18,18,18,19,21,21,23,23,23,21,21,20,20,20,19,13,13,12,11,
    raw_og[2017, 'humi'] = 68,73,73,70,76,78,76,68,47,42,34,25,24,26,23,30,30,30,29,60,67,72,
    raw_og[2017, 'wind'] = 20,22,20,22,19,19,15,20,28,24,26,35,22,28,20,26,15,17,26,24,17,30,26,

    ret : dict[int,Weather] = {}
    for yr in [2015, 2016, 2017]:
        yr_dict = {}
        for prop, (th1, th2) in [
            ('temp', (11.8, 17.1)),
            ('humi', (43.1, 57.0)),
            ('wind', (16.2, 22.6)),
        ]:
            dat = np.mean(raw_og[yr, prop])
            if   dat < th1:  lev = 'lo'
            elif dat >= th2: lev = 'hi'
            else:            lev = 'me'
            yr_dict[prop] = lev
        ret[yr] = Weather(**yr_dict)
    return ret


__ORIGINAL_WEATHER = __original_weather()

def reverse_effect(row:pd.Series):
    row['Time'] /= __ORIGINAL_WEATHER[row['Year']].effect(row['Gender'])
    return row