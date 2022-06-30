#!/usr/bin/env python3


from collections import namedtuple
import sys


# Computational Model: DFA
DFA = namedtuple('DFA', ['delta', 'final'])
ZERO, ONE, BLANK = '0', '1', '.'


def encode(dfa, binstr=''):
    '''converts DFA model to binary representation'''

    convert = lambda offset: ONE * (offset + 1) + ZERO

    for (current, symbol), successor in dfa.delta.items():
        binstr += ''.join(list(map(convert, [current, symbol, successor]))) + ZERO

    binstr += ZERO

    binstr += ''.join(list(map(convert, dfa.final)))

    return binstr


# DFA Representation
DFA.__repr__ = encode


# States
q0, q1, q2, q3, q4, q5, q6, q7 = list(range(8))


XOR_DFA = DFA(
    dict([
        ((q0, 0), q0), ((q0, 1), q1),
        ((q1, 0), q1), ((q1, 1), q0),
    ]),
    [q1]
)


F_DFA = DFA(
    dict([
        ((q0, 0), q2), ((q0, 1), q3),
        ((q1, 0), q0), ((q1, 1), q3),
        ((q2, 0), q3), ((q2, 1), q1),
        ((q3, 0), q3), ((q3, 1), q3),
    ]),
    [q0, q1]
)


ZO_DFA = DFA(
    dict([
        ((q0, 0), q1), ((q0, 1), q2),
        ((q1, 0), q1), ((q1, 1), q3),
        ((q2, 0), q2), ((q2, 1), q2),
        ((q3, 0), q1), ((q3, 1), q3),
    ]),
    [q3]
)
