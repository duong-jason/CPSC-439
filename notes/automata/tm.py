#!/usr/bin/env python3

from collections import namedtuple

DFA = namedtuple('DFA', ['T', 'S'])

def encode(M):
    '''converts DFA model to binary representation'''
    code = ''
    for (current, symbol), successor in M.T.items():
        code += ''.join(list(map(lambda b: '1' * (b + 1) + '0',
                                 [current, symbol, successor])))
    code += '0' + ''.join(list(map(lambda b: '1' * (b + 1) + '0', M.S)))
    return code

DFA.__repr__ = encode

#_____________________________________________________________________________

q0, q1, q2, q3 = list(range(4))

δ = dict([
    ((q0, 0), q0), ((q0, 1), q1),
    ((q1, 0), q1), ((q1, 1), q0),
])

blank = '_'

#_____________________________________________________________________________

class HaltExecution(Exception):
    '''halts the turing machine'''
    pass


class TuringMachine:
    '''turing machine that simulates a dfa'''

    def __init__(self, input):
        self._active = 0
        self._head = [-1, -1, -1, -1]
        self._tape = self.extract_tape(input)

        print('TAPE:', self._tape)

    @property
    def tape(self):
        '''returns the current working tape'''
        return self._tape[self._active]

    @property
    def head(self):
        '''returns the current working head'''
        return self._head[self._active]

    @head.setter
    def head(self, value=0):
        '''modifies the value of the current head'''
        self._head[self._active] = value

    @property
    def symbol(self):
        '''returns the symbol under the tape head'''
        return self.tape[self.head]

    @symbol.setter
    def symbol(self, value=None):
        '''writes the symbol under the tape head'''
        self._tape[self._active][self._head[self._active]] = value

    def __str__(self):
        '''returns the turing machine output'''
        return ''.join(self._tape[2])

    def __next__(self):
        '''moves the tape position to the right one cell'''
        self.head += 1

    def __prev__(self):
        '''moves the tape position to the left one cell'''
        self.head = max(0, self.head - 1)

    def extract_tape(self, stream: str):
        head, tape = 0, [[], [], [], [0]]

        for char in stream:
            if char == ' ': head += 1
            else: tape[head].append(char)

        return tape

    def GET(self, tape=None):
        if tape == 'dfa':
            self._active = 0
        elif tape == 'input':
            self._active = 1
        elif tape == 'work':
            self._active = 2
        elif tape == 'state':
            self._active = 3

        self.__next__()
        return self.symbol

    def transition(self, state, symbol):
        self._active = 0
        pass

    def run(self):
        '''executes the turing machine'''
        try:
            while True:
                a, b, action = transition(
                    self.GET('state'), self.GET('input')
                )

                if action == 'L':
                    self.__prev__()
                elif action == 'R':
                    self.__next__()
                elif action == 'S':
                    continue
                elif action == 'H':
                    raise HaltExecution()
        except HaltExecution:
            return str(self)

#_____________________________________________________________________________

if __name__ == '__main__':
    XOR_DFA = DFA(δ, [q1])
    print(f'XOR-DFA: {XOR_DFA!r}')

    string = '0010101'
    input = f'{XOR_DFA!r} {string}'

    M = TuringMachine(input)
    #print('OUTPUT:', str(M))
