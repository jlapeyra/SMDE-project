TOTAL_LENGTH = 42.195 #km marathon
#points = [0, 5, 10, 15, 20, 25, 27.5, 30, 35, 37.5, 40, TOTAL_LENGTH]

points = [0, 5, 10, 15, 20, 25, 30, 35, 40, TOTAL_LENGTH]
stretches = list(zip(points[:-1], points[1:]))

def primary_col(point):
    if point == TOTAL_LENGTH:
        return 'Official Time'
    #if point == TOTAL_LENGTH/2: 
    #   return 'Half'
    return f'{point}K'

def col(point):
    return f'{point}K'

def stretch_col(start, end):
    return f'{start}-{end}K'