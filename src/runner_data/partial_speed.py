import km_divisions as km
import groups
import pandas as pd


data = pd.read_csv('data/runner_data.csv')
df = pd.DataFrame()
for col in groups.COLUMNS:
    df[col] = data[col]

avg_speed = km.TOTAL_LENGTH / data['Time']
for km_start, km_end in km.stretches:
    partial_time = data[km.col(km_end)] - data[km.col(km_start)]
    partial_length = km_end - km_start
    partial_speed = partial_length / partial_time
    df[km.stretch_col(km_start, km_end)] = partial_speed/avg_speed


df.to_csv('data/partial_relative_speed.csv', index=False, float_format='%.5f')