import pandas as pd
from itertools import product
from functools import reduce
import operator

COLUMNS = ['Gender', 'Age', 'Time']

CONDITIONS = {
    'Gender' : [
        ('M', lambda data: data == 'M'),
        ('F', lambda data: data == 'F')
    ],
    'Age' : [
        ('18-30', lambda data: data <= 30),
        ('31-50', lambda data: (data > 30) & (data <= 50)),
        ('51+', lambda data: data > 50)
    ],
    'Time' : [
        ('<3h', lambda data:  (data < 3*60)),
        ('3-4h', lambda data: (data >= 3*60) & (data < 4*60)),
        ('4-5h', lambda data: (data >= 4*60) & (data < 5*60)),
        ('>5h', lambda data:  (data >= 5*60))
    ]
}

def getCompositeGroup(row, columns=COLUMNS):
    return tuple(getGroup(row[col], col) for col in columns)

def getGroup(value, column):
    assert column in COLUMNS, f'Invalid column {column}'
    for label, condition in CONDITIONS[column]:
        if condition(value):
            return label
    raise Exception()
    

def getGroups(data, columns=COLUMNS):
    '''
    Get groups of runners based on the specified columns
    '''
    assert set(columns) <= set(COLUMNS), f'Invalid columns: {columns}'

    conditions = [
        [
            (label, func(data[col]))
            for label, func in CONDITIONS[col]
        ]
        for col in columns
    ]

    groups : dict[tuple[str,...], pd.Series[bool]] = {}

    for prod in product(*conditions):
        label = tuple(l for l,_ in prod) 
        # e.g. ('M', '18-30', '<3h')
        condition = reduce(operator.and_, (b for _,b in prod), True) 
        # e.g. (data['Gender'] == 'M') & (data['Age'] <= 30) & (data['Time'] < 3*60)
        groups[label] = condition

    return groups


if __name__ == '__main__':
    # Load the data
    data = pd.read_csv('data/runner_data.csv')

    for group, df in getGroups(data).items():
        #label = ''.join(g.ljust(6) for g in group)
        gender, age, time = group
        label = gender.ljust(1+2) + age.ljust(5+2) + time.ljust(4+1)
        print(label, sum(df), sep=': ')