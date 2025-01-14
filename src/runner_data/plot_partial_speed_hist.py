import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import groups
import km_divisions as km
from scipy.stats import gaussian_kde

DATA = pd.read_csv('data/partial_relative_speed.csv')
time_groups = groups.getGroups(DATA, ['Time'])

stretches = [km.stretch_col(km_start, km_end) for km_start, km_end in km.stretches]


# Crea la figura i els subplots
fig, axes = plt.subplots(len(time_groups), len(stretches), figsize=(8, 8))


XMIN, XMAX = 0.6, 1.4
YMIN, YMAX = 0, 12
x = np.linspace(XMIN, XMAX, 100)

# Omple els subplots
for i, group in enumerate(time_groups.values()):
    for j, stretch in enumerate(stretches):
        data = DATA[group][stretch]
        kde = gaussian_kde(list(filter(pd.notna, data)))
        axes[i, j].set_xlim(XMIN, XMAX)
        axes[i, j].set_ylim(YMIN, YMAX)
        axes[i, j].plot(x, kde.pdf(x))
        axes[i, j].hist(data, range=(XMIN, XMAX), bins=16, alpha=0.7, density=True)

# Afegeix les anotacions de fila
for ax, row_label in zip(axes[:, 0], time_groups.keys()):
    ax.annotate(','.join(row_label), xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 5, 0),
                xycoords=ax.yaxis.label, textcoords='offset points',
                ha='right', va='center', fontsize=12)

# Afegeix les anotacions de columna
for ax, col_label in zip(axes[0, :], stretches):
    ax.annotate(col_label, xy=(0.5, 1), xytext=(0, 5),
                xycoords='axes fraction', textcoords='offset points',
                ha='center', va='baseline', fontsize=12)

# Mostra la figura
fig.suptitle('Probability density of relative partial speed per stretch and level')
plt.show()






