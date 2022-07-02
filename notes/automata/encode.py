from collections import namedtuple
from state import *


# Computational Model: DFA
DFA = namedtuple('DFA', ['delta', 'final'])

def encode(dfa, binstr=''):
    '''converts DFA model to binary representation'''
    convert = lambda offset: ONE * (offset + 1) + ZERO

    for (current, symbol), successor in dfa.delta.items():
        binstr += ''.join(list(map(convert, [current, symbol, successor]))) + ZERO
    binstr += ZERO + ''.join(list(map(convert, dfa.final)))
    return binstr


# DFA Representation
DFA.__repr__ = encode


# States
q0, q1, q2, q3, q4, q5, q6, q7 = list(range(8))


XOR = DFA(
    dict([
        ((q0, 0), q0), ((q0, 1), q1),
        ((q1, 0), q1), ((q1, 1), q0),
    ]),
    [q1]
)


ZOZ = DFA(
    dict([
        ((q0, 0), q2), ((q0, 1), q3),
        ((q1, 0), q0), ((q1, 1), q3),
        ((q2, 0), q3), ((q2, 1), q1),
        ((q3, 0), q3), ((q3, 1), q3),
    ]),
    [q0]
)


ZO = DFA(
    dict([
        ((q0, 0), q1), ((q0, 1), q2),
        ((q1, 0), q1), ((q1, 1), q3),
        ((q2, 0), q2), ((q2, 1), q2),
        ((q3, 0), q1), ((q3, 1), q3),
    ]),
    [q3]
)

COUNTER = DFA(
    dict([
        ((q0, 0), q1), ((q0, 1), q7),
        ((q1, 0), q2), ((q1, 1), q0),
        ((q2, 0), q3), ((q2, 1), q1),
        ((q3, 0), q4), ((q3, 1), q2),
        ((q4, 0), q5), ((q4, 1), q3),
        ((q5, 0), q6), ((q5, 1), q4),
        ((q6, 0), q7), ((q6, 1), q5),
        ((q7, 0), q0), ((q7, 1), q6),
    ]),
    [q5, q6, q7]
)

MULTI3 = DFA(
    dict([
        ((q0, 0), q0), ((q0, 1), q1),
        ((q1, 0), q2), ((q1, 1), q0),
        ((q2, 0), q1), ((q2, 1), q2),
    ]),
    [q0]
)
