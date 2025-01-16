raw = '''
M lo temp 361
M me temp 358
M hi temp 353
F lo temp 278
F me temp 272
F hi temp 264

M lo humi 354
M me humi 362
M hi humi 362
F lo humi 271
F me humi 280
F hi humi 270

M lo wind 348
M me wind 361
M hi wind 372
F lo wind 269
F me wind 279
F hi wind 277
'''

# y = a*x + b

a = (300-200)/(240-511)
b = 200 - a*511


with open('data/effect.csv', 'w', encoding='utf 8') as f:
    print('gender,level,prop,value', file=f)
    for line in raw.splitlines():
        if line:
            row = line.split()
            x = int(row[-1])
            y = a*x + b
            row[-1] = round(y, 1)
            print(*row, sep=',', file=f)
