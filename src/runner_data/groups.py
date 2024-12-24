import pandas as pd
from itertools import product
from km_divisions import TOTAL_LENGTH_COL
from functools import reduce
import operator

# Load the data
data = pd.read_csv('data/runner_data.csv')

# Convert time from minutes to hours
data['Time_hours'] = data[TOTAL_LENGTH_COL] / 60

# Define the conditions for splitting
conditions = {
    'gender': [
        ('M', data['Gender'] == 'M'),
        ('F', data['Gender'] == 'F')
    ],
    'age': [
        ('18-30', data['Age'] <= 30),
        ('31-50', (data['Age'] > 30) & (data['Age'] <= 50)),
        ('51+', data['Age'] > 50)
    ],
    'time': [
        ('<3h',  (data['Time_hours'] < 3)),
        ('3-4h', (data['Time_hours'] >= 3) & (data['Time_hours'] < 4)),
        ('4-5h', (data['Time_hours'] >= 4) & (data['Time_hours'] < 5)),
        ('>5h',   data['Time_hours'] >= 5)
    ]
}

groups = {}

for prod in product(*conditions.values()):
    label = tuple(x[0] for x in prod) # e.g. ('M', '18-30', '<3h')
    condition = reduce(operator.and_, (x[1] for x in prod)) # e.g. (data[Gender] == 'M') & (data[Age] <= 30) & (data[Time_hours] < 3)
    groups[label] = data[condition]







# Apply the conditions and labels to create a new column
#data['Group'] = pd.cut(data.index, bins=len(conditions), labels=labels)

# Save the split data into separate CSV files
#for label in labels:
#    subset = data[data['Group'] == label]
#    subset.to_csv(f'data/{label}.csv', index=False)