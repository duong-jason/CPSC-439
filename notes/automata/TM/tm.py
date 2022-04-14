#!/usr/bin/env python3


import dfa


Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8 = list(range(1, 9))
model, input, work, state = 0, 1, 2, 3


class HaltExecution(Exception):
    '''halting instruction'''
    pass


class TuringMachine:
    '''turing machine that simulates a dfa'''

    def __init__(self, input):
        self._active = 0
        self._head = [-1, -1, -1, -1]
        self._tape = self.init_tape(input)

        print('input:', input)
        print('tape:', self._tape)

    @property
    def active(self):
        '''represents the current working tape'''
        return self._active

    @active.setter
    def active(self, value=0):
        '''modifies the current working tape'''
        self._active = value

    @property
    def tape(self):
        '''returns the tape'''
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
        self.head = max(-1, self.head - 1)

    def init_tape(self, stream: str):
        tape, pos = [[], [], [], [Q1]], 0
        for head in range(len(stream)):
            if stream[head] == '_': pos += 1
            else: tape[pos].append(int(stream[head]))
        return tape

    def rewind_tape(self, tape=None):
        '''resets the head position for the working tape'''
        while self.head != -1:
            self.__prev__()

    def get_tape(self, tape=None):
        self.active = tape
        self.__next__()
        return self.symbol

    def write_tape(self, tape=None, value=0):
        self.active = tape
        if self.head > len(self.tape):
            self.tape.append('*')
        self.head = value

    def transition(self, state, symbol):
        self.active = model

        if (state, symbol) == (Q1, 1):
            self.active = work
            self.write_tape(state, Q2)

        return self.get_tape(state), self.get_tape(input)

        '''
        (1)0(1)0[1]0   (1)0(11)0[11]0  (11)0(1)0[11]0   (11)0(11)0[1]0    00    [11]


        1. read (current state, input symbol)
        2. read dfa tape
            a. while symbol not '0':
                x = count number of ones
            b. write to working_tape = x
            c.

        dfa:     [10101000110101101100011011010110001101101101000110]
        input:   [0 010101]
        working: []
        state:   [1]


        working {
            ONE, TWO, THREE
        }


        states {
            8 states -> 8 transitions -> 3 bits the represent each digit

            q00 q01 q10 q11 = { 0, 1, 2, 3 }

        }


        '''
        return state, symbol

    def run(self):
        '''executes the turing machine'''
        try:
            while True:
                self.transition(self.get_tape(state), self.get_tape(input) + 1)
                break

                if action == 'L':
                    self.__prev__()
                elif action == 'R':
                    self.__next__()
                elif action == 'S':
                    continue
                elif action == 'H':
                    raise HaltExecution()
        except HaltExecution:
            # write accept/reject at the end of the tape
            return str(self)


if __name__ == '__main__':
    source = '0010101'
    M = TuringMachine(f'{dfa.xor!r}_{source}')
    M.run()
