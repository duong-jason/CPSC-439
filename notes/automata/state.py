TAPE_LEN = 4
SHOW_HEAD = 0
SLOW, MEDIUM, FAST = 0.5, 0.01, 0.001

# ___STATES___
ZERO = '0'
ONE = '1'
BLANK = '.'
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
