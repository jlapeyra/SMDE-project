import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/..'))

from race.groups import *


if __name__ == '__main__':
    # Load the data
    data = pd.read_csv('data/runner_data.csv')

    for group, df in getGroups(data).items():
        #label = ''.join(g.ljust(6) for g in group)
        gender, age, time = group
        label = gender.ljust(1+2) + age.ljust(5+2) + time.ljust(4+1)
        print(label, sum(df), sep=': ')