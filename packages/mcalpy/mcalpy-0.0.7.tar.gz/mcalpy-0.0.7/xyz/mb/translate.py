import xyz.mb.dicts

def rl(st: str) -> str:
    """
    It is translate English or integer into morse code.
    """
    result = str()
    for i in list(st):
        result = result + '%s' % xyz.mb.dicts.KEY[i] + ' '
    return result.strip()