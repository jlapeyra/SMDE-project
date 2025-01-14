import pandas as pd
from itertools import combinations, product
from functools import reduce
import operator
import utils

df = pd.read_csv('data/meteocat/simplified.csv')

TEMPERATURE = 'temp'
HUMIDITY = 'humi'
WIND = 'wind'

LOW = 'lo'
MEDIUM = 'me'
HIGH = 'hi'

properties = [TEMPERATURE, HUMIDITY, WIND]
levels = [LOW, MEDIUM, HIGH]


# Temperature: low (5.0 – 11.7°C), medium (11.8 – 17.0°C), high (17.1 – 24.5°C)
# Relative humidity: low (26 – 43%), medium (43.1 – 56.9%), high (57 – 100%)
# Wind speed: low (8.1 – 16.1 km/h), medium (16.2 – 22.5 km/h), high (22.6 – 48.3 km/h)
groups = {}
for prop_id, prop_name, (th1, th2) in [
    (TEMPERATURE, 'Temperature', (11.8, 17.1)),
    (HUMIDITY,    'Humidity',    (43.1, 57.0)),
    (WIND,        'Wind',        (16.2, 22.6)),
]:
    groups[LOW, prop_id]    = df[prop_name] < th1
    groups[MEDIUM, prop_id] = (th1 <= df[prop_name]) & (df[prop_name] < th2)
    groups[HIGH, prop_id]   = th2 <= df[prop_name]

MONTHS = list(range(1, 12+1))

# data = {}
# for n in [0, 1, 2, 3]:
#     for props in combinations(properties, n):
#         for levs in product(*[levels]*n):
#             label = '+'.join(f'{l}-{p}' for (l,p) in zip(levs, props))
#             print(label)
#             combined_group = reduce(operator.and_, (groups[(l,p)] for (l,p) in zip(levs, props)), True)
#             rates = []
#             for month in MONTHS:
#                 month_group = df['Month'] == month
#                 rate = sum(combined_group & month_group)#/sum(month_group)
#                 rates.append(rate)
#             data[label] = rates

data = {}
for prop in properties:
    for lev in levels:
        label = f'{lev}-{prop}'
        print(label)
        lev_group = groups[lev,prop]
        rates = []
        for month in MONTHS:
            month_group = df['Month'] == month
            rate = sum(lev_group & month_group)/sum(month_group)
            rates.append(rate)
        data[label] = rates


pd.DataFrame(data, index=MONTHS).map(utils.float_formatter(6)).to_csv('data/meteocat/levels.csv')




