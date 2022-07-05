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


F = DFA(
    dict([
        ((q0, a), q2), ((q0, b), q3),
        ((q1, a), q0), ((q1, b), q3),
        ((q2, a), q3), ((q2, b), q1),
        ((q3, a), q3), ((q3, b), q3),
    ]),
    [q0]
)
