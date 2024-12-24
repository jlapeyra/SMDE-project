TOTAL_LENGTH = 42.195 #km marathon
km_points = [0, 5, 10, 15, 20, 25, 27.5, 30, 35, 37.5, 40, TOTAL_LENGTH]

def km_col(km_point):
    return f'{km_point}K'

def streach_col(km_point_start, km_point_end):
    return f'{km_point_start}K-{km_point_end}K'

TOTAL_LENGTH_COL = f'{TOTAL_LENGTH}K'