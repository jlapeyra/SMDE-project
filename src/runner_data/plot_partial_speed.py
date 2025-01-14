import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import groups
import km_divisions as km

data = pd.read_csv('data/partial_relative_speed.csv')
#per_gender_age = groups.getGroups(data, ['Gender', 'Age'])
time_groups = groups.getGroups(data, ['Time'])

cols = [km.stretch_col(km_start, km_end) for km_start, km_end in km.stretches]

means = {}
stdevs = {}

for label, condition in time_groups.items():
    label = label[0]
    group = data[condition]
    #avg_speed = km.TOTAL_LENGTH / group['Time']
    means[label] = [
        group[col].mean() for col in cols
    ]
    stdevs[label] = [
        group[col].std() for col in cols
    ]

for plt_data, name in ((means, 'mean'), (stdevs, 'stdev')):
    for label, plt_data_line in plt_data.items():
        plt.plot(plt_data_line, label=label)
    plt.xticks([i-0.5 for i in range(len(km.points))], km.points)
    plt.xlabel('km point')
    plt.ylabel(f'relative speed between km points ({name})')
    plt.legend().set_title('total time')
    plt.savefig(f'plots/partial_relative_speed_{name}.png')
    plt.show()



