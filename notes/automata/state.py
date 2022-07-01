K = 4
SHOW_HEAD = 0
SLOW, MEDIUM, FAST = 0.5, 0.01, 0.001

# __STATES___
START = '▷'
ACCEPT = True
REJECT = False
# __DIRECTIONS___
LEFT = '<'
RIGHT = '>'
STAY = '-'
# __REGISTERS___
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
