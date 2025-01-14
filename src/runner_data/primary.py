import km_divisions as km
import pandas as pd
import glob
import utils

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

df_list = []
#for path in glob.glob('data/primary/marathon_results_*.csv'):
for year in [2015, 2016, 2017]:
    path = f'data/primary/marathon_results_{year}.csv'
    df_in = pd.read_csv(path)

    df_out = pd.DataFrame(index=df_in.index)
    df_out['Year'] = year
    df_out['Age'] = df_in['Age']
    df_out['Gender'] = df_in['M/F']
    df_out['Time'] = df_in['Official Time'].apply(timeFormatToMinutes)
    df_out['Ranking'] = df_in['Overall']
    df_out['Ranking gender'] = df_in['Gender']
    df_out['Ranking division'] = df_in['Division']
    df_out['0K'] = 0
    for km_point in km.points[1:]:
        col_in = km.primary_col(km_point)
        col_out = km.col(km_point)
        df_out[col_out] = df_in[col_in].apply(timeFormatToMinutes)
    df_list.append(df_out)

df = pd.concat(df_list).reset_index(drop=True)

df.map(utils.float_formatter(3)).to_csv('data/runner_data.csv', index=False)


# km_points_idx = {}
# for km_point in km.points:
#     for i in range(len(km_point_columns)):
#         if km_point_columns[i][1] == km_point:
#             km_points_idx[km_point] = i,i
#             break
#         elif km_point_columns[i][1] > km_point:
#             km_points_idx[km_point] = i-1,i
#             break

# def closestNonNA(row, start, inc):
#     for col, val in km_point_columns[start::inc]:
#         if pd.notna(row[col]):
#             return col, val
#     return None, None

# def estimateTime(km_point, row):
#     '''
#     estimate the time taken to reach each kilometer point if the time is not recorded in the data
#     '''
#     prev, post = km_points_idx[km_point]
#     col0, val0 = closestNonNA(row, prev, -1)
#     col1, val1 = closestNonNA(row, post, +1)
#     if None in (col0, col1):
#         return pd.NA
#     elif col0 == col1: 
#         return row[col0]
#     else:
#         return row[col0] + (row[col1]-row[col0])*(km_point-val0)/(val1-val0)
    
#for km_point in km_points:
#    df_out[f'{km_point}K'] = df_in.apply(lambda row: estimateTime(km_point, row), axis=1)



