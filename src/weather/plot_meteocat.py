import pandas as pd
import matplotlib.pyplot as plt

# Carregar el fitxer CSV en un DataFrame
df = pd.read_csv('data/meteocat/levels.csv', index_col=0)


# Crear el barplot
fig, ax = plt.subplots()

bar_positions = range(12)

# Plotejar les barres
prop = 'wind'

ax.bar(bar_positions, df['lo-{}'.format(prop)], 
       label='Low', color='cornflowerblue')
ax.bar(bar_positions, df['me-{}'.format(prop)], bottom=df['lo-{}'.format(prop)], 
       label='Medium', color='limegreen')
ax.bar(bar_positions, df['hi-{}'.format(prop)], bottom=df['lo-{}'.format(prop)] + df['me-{}'.format(prop)], 
       label='High', color='orange')

# Afegir etiquetes i títol
ax.set_xlabel('Month')
ax.set_ylabel('Share of days')
ax.set_title('Wind level')
ax.set_xticks(bar_positions)
ax.set_xticklabels(df.index)
ax.legend()

# Mostrar el gràfic
plt.tight_layout()
plt.show()