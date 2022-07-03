from string import ascii_uppercase

TAPE_LEN = 4
SHOW_HEAD = 0
SLOW, MEDIUM, FAST = 0.5, 0.01, 0.001

# ___SYMBOLS___
ZERO  = '0'
ONE   = '1'
BLANK = '.'  # symbol to keep track of the end of tape
COPY  = "*"  # symbol under tape's head position
SEP   = "#"  # symbol to keep track between symbols on tapes
INCR  = '+'  # symbol obtained by adding the <HEAD> symbol (must be on the same tape)
EQ    = '!'  # symbol that accepts all symbols under a tape's head position where the '!' was specified is equal
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

class StateError(HaltProcess):
    pass

class MoveError(HaltProcess):
    pass

class CellFault(HaltProcess):
    pass