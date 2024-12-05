
def join(a:str|None, b:str|None):
    if a and b:
        return str(a) + ' ' + str(b)
    if a:
        return str(a)
    if b:
        return str(b)
    return ''
