
def join_nullables(a:str|None, b:str|None):
    if a and b:
        return a + ' ' + b
    if a:
        return a
    if b:
        return b
    return ''
