from string import ascii_uppercase, ascii_lowercase

TAPE_LEN = 4

# ___SYMBOLS___
a, b, c, d, e, f, g, h, i ,j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = list(ascii_lowercase)
VAL = {letter: value for value, letter in enumerate(ascii_lowercase)}

BLANK = '.'  # symbol to keep track of the end of tape
COPY  = "*"  # symbol under tape's head position
SEP   = "#"  # symbol to keep track between symbols on tapes
INCR  = '+'  # symbol obtained by adding the <HEAD> symbol (must be on the same tape)
EQ    = '='  # symbol that accepts any symbol under a tape's head position where the '=' specifies equality
NEG   = '!'  # symbols that accepts any symbol under a tape's head position where the '!' specifies negality
# ___STATES___
START = '▷'
ACCEPT = True
REJECT = False
# ___DIRECTIONS___
LEFT  = '<'
RIGHT = '>'
STAY  = '-'
# ___REGISTERS___
REG = list(ascii_uppercase)

class HaltProcess(Exception):
    pass

class SymbolError(HaltProcess):
    pass

class MoveError(HaltProcess):
    pass

class CellFault(HaltProcess):
    pass

def blue(text):
    return "\033[96m" + text + "\033[0m"

def red(text):
    return "\033[91m" + text + "\033[0m"

def green(text):
    return "\033[32m" + text + "\033[0m"

def yellow(text):
    return "\033[93m" + text + "\033[0m"
