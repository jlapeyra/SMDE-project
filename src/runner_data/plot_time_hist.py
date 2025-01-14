import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import seaborn as sns
import numpy as np
import groups



PINK = (1, 0.2, 0.2)
BLUE = (0.2, 0.2, 1)
WHITE = (1, 1, 1)
    
data = pd.read_csv('data/runner_data.csv')
data_hours = data['Time'] / 60

#kde = gaussian_kde(data_hours)
#plt.hist(data_hours, bins=40, density=True, alpha=0.6)
x = np.linspace(2, 6, 100)


for (gender, age), group_vec in groups.getGroups(data, ['Gender', 'Age']).items():
    group_data_hours = data_hours[group_vec]
    kde = gaussian_kde(group_data_hours)
    plt.plot(
        x, kde.pdf(x), 
        label=f'{gender}, {age}', 
        color={'M': BLUE, 'F': PINK}[gender],
        alpha={'18-30':1, '31-50':0.65, '51+':0.3}[age]
    )
    print(age, gender, len(group_data_hours))
plt.xlabel('Time (hours)')
plt.ylabel('Density')
plt.title('Probablility density function')
plt.legend()
plt.show()


