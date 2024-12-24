from km_divisions import km_points, TOTAL_LENGTH
import pandas as pd
import glob

def timeFormatToMinutes(time:str):
    'convert time in the format hh:mm:ss to minutes'
    return timeFormatToSeconds(time)/60

def timeFormatToSeconds(time:str):
    'convert time in the format hh:mm:ss to seconds'
    if time == '-':
        return pd.NA
    time = time.split(':')
    return int(time[0])*3600 + int(time[1])*60 + int(time[2])

def formatTime(time:int):
    'convert time in seconds to the format hh:mm:ss'
    return f'{time//3600:02}:{time%3600//60:02}:{time%60:02}'

km_point_columns = [
    ('0K', 0),
    ('5K', 5),
    ('10K', 10),
    ('15K', 15),
    ('20K', 20),
    ('Half', TOTAL_LENGTH/2),
    ('25K', 25),
    ('30K', 30),
    ('35K', 35),
    ('40K', 40),
    ('Official Time', TOTAL_LENGTH)
]

km_points_idx = {}
for km_point in km_points:
    for i in range(len(km_point_columns)):
        if km_point_columns[i][1] == km_point:
            km_points_idx[km_point] = i,i
            break
        elif km_point_columns[i][1] > km_point:
            km_points_idx[km_point] = i-1,i
            break

def closestNonNA(row, start, inc):
    for col, val in km_point_columns[start::inc]:
        if pd.notna(row[col]):
            return col, val
    return None, None

def estimateTime(km_point, row):
    '''
    estimate the time taken to reach each kilometer point if the time is not recorded in the data
    '''
    prev, post = km_points_idx[km_point]
    col0, val0 = closestNonNA(row, prev, -1)
    col1, val1 = closestNonNA(row, post, +1)
    if None in (col0, col1):
        return pd.NA
    elif col0 == col1: 
        return row[col0]
    else:
        return row[col0] + (row[col1]-row[col0])*(km_point-val0)/(val1-val0)

#estimate time taken to reach each kilometer point based on the kilometer points recorded in the data
df_list = []
for path in glob.glob('data/primary/marathon_results_*.csv'):
    df_in = pd.read_csv(path)
    df_in['0K'] = 0
    for col,_ in km_point_columns[1:]:
        df_in[col] = df_in[col].apply(timeFormatToMinutes)
    df_out = pd.DataFrame()
    df_out['Age'] = df_in['Age']
    df_out['Gender'] = df_in['M/F']
    for km_point in km_points:
        df_out[f'{km_point}K'] = df_in.apply(lambda row: estimateTime(km_point, row), axis=1)
    df_list.append(df_out)

df = pd.concat(df_list).reset_index(drop=True)
df.to_csv('data/curated/runner_data.csv', index=False, float_format='%.2f')

    



