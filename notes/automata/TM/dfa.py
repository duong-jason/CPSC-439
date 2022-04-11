from collections import namedtuple

DFA = namedtuple('DFA', ['T', 'S'])

q0, q1, q2, q3 = list(range(4))

def encode(M):
    '''converts DFA model to binary representation'''
    code = ''
    for (current, symbol), successor in M.T.items():
        code += ''.join(list(map(lambda b: '1' * (b + 1) + '0', [current, symbol, successor])))
        code += '00'
        code += ''.join(list(map(lambda b: '1' * (b + 1) + '0', M.S)))
    return code

DFA.__repr__ = encode


δ = dict([
    ((q0, 0), q0), ((q0, 1), q1),
    ((q1, 0), q1), ((q1, 1), q0),
])

xor = DFA(δ, [q1])

δ = dict([
    ((q0, 0), q2), ((q0, 1), q3),
    ((q1, 0), q0), ((q1, 1), q3),
    ((q2, 0), q3), ((q2, 1), q1),
    ((q3, 0), q3), ((q3, 1), q3),
])

f = DFA(δ, [q0])
