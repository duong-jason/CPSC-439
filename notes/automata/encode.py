from collections import namedtuple
from state import *


# Computational Model: DFA
DFA = namedtuple('DFA', ['delta', 'final'])

def encode(dfa, binstr=''):
    '''converts DFA model to binary representation'''
    convert = lambda offset: '1' * (offset + 1) + '0'

    for (current, symbol), successor in dfa.delta.items():
        binstr += ''.join(list(map(convert, [current, VAL[symbol], successor]))) + '0'

    return binstr + '0' + ''.join(list(map(convert, dfa.final)))


# DFA Representation
DFA.__repr__ = encode


# States
q0, q1, q2, q3, q4, q5, q6, q7, q8 = list(range(9))


XOR = DFA(
    dict([
        ((q0, a), q0), ((q0, b), q1),
        ((q1, a), q1), ((q1, b), q0),
    ]),
    [q1]
)


ZOZ = DFA(
    dict([
        ((q0, a), q2), ((q0, b), q3),
        ((q1, a), q0), ((q1, b), q3),
        ((q2, a), q3), ((q2, b), q1),
        ((q3, a), q3), ((q3, b), q3),
    ]),
    [q0]
)


ZO = DFA(
    dict([
        ((q0, a), q1), ((q0, b), q2),
        ((q1, a), q1), ((q1, b), q3),
        ((q2, a), q2), ((q2, b), q2),
        ((q3, a), q1), ((q3, b), q3),
    ]),
    [q3]
)

COUNTER = DFA(
    dict([
        ((q0, a), q1), ((q0, b), q7),
        ((q1, a), q2), ((q1, b), q0),
        ((q2, a), q3), ((q2, b), q1),
        ((q3, a), q4), ((q3, b), q2),
        ((q4, a), q5), ((q4, b), q3),
        ((q5, a), q6), ((q5, b), q4),
        ((q6, a), q7), ((q6, b), q5),
        ((q7, a), q0), ((q7, b), q6),
    ]),
    [q5, q6, q7]
)

MULTI3 = DFA(
    dict([
        ((q0, a), q0), ((q0, b), q1),
        ((q1, a), q2), ((q1, b), q0),
        ((q2, a), q1), ((q2, b), q2),
    ]),
    [q0]
)

TWO_ZO = DFA(
    dict([
        ((q0, a), q3), ((q0, b), q1),
        ((q1, a), q4), ((q1, b), q2),
        ((q2, a), q5), ((q2, b), q2),
        ((q3, a), q6), ((q3, b), q4),
        ((q4, a), q7), ((q4, b), q5),
        ((q5, a), q8), ((q5, b), q5),
        ((q6, a), q6), ((q6, b), q7),
        ((q7, a), q7), ((q7, b), q8),
        ((q8, a), q8), ((q8, b), q8),
    ]),
    [q8]
)
