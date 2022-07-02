TAPE_LEN = 4
SHOW_HEAD = 1
SLOW, MEDIUM, FAST = 0.5, 0.01, 0.001

# ___SYMBOLS___
ZERO = '0'
ONE = '1'
BLANK = '.'  # symbol to keep track of the end of tape
COPY = "*"   # symbol under tape's head position
SEP = "#"    # symbol to keep track between symbols on tapes
INCR = '+'    # symbol obtained by adding the <HEAD> symbol (must be on the same tape)
EQ = '!'    # symbol that accepts all symbols under a tape's head position where the '!'
             # was specified is equal
# ___STATES___
START = '▷'
ACCEPT = True
REJECT = False
# ___DIRECTIONS___
LEFT = '<'
RIGHT = '>'
STAY = '-'
# ___REGISTERS___
R1 = 'A'
R2 = 'B'
R3 = 'C'
R4 = 'D'
R5 = 'E'
R6 = 'F'
R7 = 'G'
R8 = 'H'


class HaltProcess(Exception):
    pass
