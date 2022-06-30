#!/usr/bin/env python3

import sys
from enum import Enum, auto
from encode import *


K = 4
SHOW_HEAD = True


class State(Enum):
    # __________________
    ZERO = '0'
    ONE = '1'
    BLANK = '.'
    # __________________
    START = '▷'
    ACCEPT = auto()
    REJECT = auto()
    # __________________
    LEFT = '<'
    RIGHT = '>'
    STAY = '-'
    # __________________
    R1 = 'A'
    R2 = 'B'
    R3 = 'C'
    R4 = 'D'
    R5 = 'E'
    R6 = 'F'
    R7 = 'G'
    R8 = 'H'

    def __str__(self):
        return str(self.value)

class TM:
    def __init__(self, input_string):
        self._tape = [list(f'▷{i}') for i in input_string.split('#') + list('A') + list(BLANK)]
        self._head = [0] * K
        self._state = 'START'
        self._steps = 0


    def __str__(self):
        '''Outputs the current tape state'''
        res = ''
        print('\033[32m' + self._state + '\033[0m')



        if SHOW_HEAD:
            for i in range(K):
                for j, cell in enumerate(self._tape[i]):
                    if j == self._head[i]:
                        res += '\033[91m' + "       v" + '\033[0m'
                    else:
                        res += " "
                res += "\n"
                res += f"\033[96mMODEL  \033[0m" if i == 0 else \
                       f"\033[96mINPUT  \033[0m" if i == 1 else \
                       f"\033[96mSTATE  \033[0m" if i == 2 else \
                       f"\033[96mMEMORY \033[0m"
                for k, cell in enumerate(self._tape[i]):
                    if k == self._head[i]:
                        res += '\033[91m' + str(cell) + '\033[0m'
                    else:
                        res += str(cell)
                res += "\n"
        else:
            for i in range(K):
                res += f"\033[96mMODEL  \033[0m" if i == 0 else \
                       f"\033[96mINPUT  \033[0m" if i == 1 else \
                       f"\033[96mSTATE  \033[0m" if i == 2 else \
                       f"\033[96mMEMORY \033[0m"
                for j, cell in enumerate(self._tape[i]):
                    if j == self._head[i]:
                        res += '\033[91m' + str(cell) + '\033[0m'
                    else:
                        res += str(cell)
                res += '\n'
        return res


    @property
    def state(self):
        return self._state


    @state.setter
    def state(self, state):
        self._state = state


    def tape(self, pos):
        '''Returns the symbol on a particular tape'''
        return self._tape[pos][self._head[pos]]


    def symbol(self, action):
        x = [str(self.tape(i)) for i in range(K)]
        y = list(action)

        z = [i for i in range(K) if y[i] == '-']

        [x.pop(i) and y.pop(i) for i in reversed(z)]

        return x == y


    def write(self, action):
        """Writes a symbol on each tape"""
        action = list(map(lambda f: State(f), list(action)))

        for i in range(K):
            if action[i] != State.STAY:
                self._tape[i][self._head[i]] = action[i]


    def move(self, action):
        """Moves the head position on each tape"""
        action = list(map(lambda f: State(f), list(action)))

        for i, move in enumerate(action):
            match move:
                case State.LEFT:
                    self._head[i] = max(0, self._head[i] - 1)
                case State.RIGHT:
                    if self._head[i] >= len(self._tape[i]) - 1:
                        self._tape[i] += BLANK
                    self._head[i] += 1
                case State.STAY:
                    self._head[i] = self._head[i]
                case _:
                    raise ValueError(f"Invalid Move: {move}")


    def T(self, x, y, z, i):
        if self.symbol(x):
            self.write(y)
            self.move(z)
            self.state = i
            return True
        return False


    def REWIND(self):
        if str(self.tape(0)) != str(State.START):
            self.move('<---')
        else:
            self._state = "START"

    def START(self):
        if self.T("▷▷▷▷", "----", ">>>>", "SCAN_STATE"): return
        if self.T("▷.--", "----", ">---", "HALT"): return
        if self.T("▷---", "----", ">---", "SCAN_STATE"): return

    def SCAN_STATE(self):
        if self.T("1--.", "---A", ">---", "SCAN_STATE"): return
        if self.T("1--A", "---B", ">---", "SCAN_STATE"): return
        if self.T("1--B", "---C", ">---", "SCAN_STATE"): return
        if self.T("1--C", "---D", ">---", "SCAN_STATE"): return
        if self.T("1--D", "---E", ">---", "SCAN_STATE"): return
        if self.T("1--E", "---F", ">---", "SCAN_STATE"): return
        if self.T("1--F", "---G", ">---", "SCAN_STATE"): return
        if self.T("1--G", "---H", ">---", "SCAN_STATE"): return
        if self.T("1--H", "----", "----", "REJECT"): return
        if self.T("0---", "----", ">---", "CHECK_STATE"): return

    def SCAN_INPUT(self):
        if self.T("1--.", "---0", ">---", "SCAN_INPUT"): return
        if self.T("1--0", "---1", ">---", "SCAN_INPUT"): return
        if self.T("1--1", "----", "----", "REJECT"): return
        if self.T("0---", "----", ">---", "CHECK_INPUT"): return

    def SCAN_FINAL(self):
        if self.T("1--.", "---A", ">---", "SCAN_FINAL"): return
        if self.T("1--A", "---B", ">---", "SCAN_FINAL"): return
        if self.T("1--B", "---C", ">---", "SCAN_FINAL"): return
        if self.T("1--C", "---D", ">---", "SCAN_FINAL"): return
        if self.T("1--D", "---E", ">---", "SCAN_FINAL"): return
        if self.T("1--E", "---F", ">---", "SCAN_FINAL"): return
        if self.T("1--F", "---G", ">---", "SCAN_FINAL"): return
        if self.T("1--G", "---H", ">---", "SCAN_FINAL"): return
        if self.T("0---", "----", "----", "CHECK_FINAL"): return

    def CHECK_STATE(self):
        if str(self.tape(2)) == str(self.tape(3)):
            self.move("--->")
            self.state = "SCAN_INPUT"
        else:
            self.move("--->")
            self.state = "NEXT_STATE"

    def CHECK_INPUT(self):
        if str(self.tape(1)) == str(self.tape(3)):
            self.move("-->>")
            self.state = "GET_STATE"
        else:
            self.move("--->")
            self.state = "NEXT_STATE"

    def CHECK_FINAL(self):
        if str(self.tape(2)) == str(self.tape(3)):
            self.state = "ACCEPT"
        else:
            self.state = "REJECT"

    def GET_STATE(self):
        if self.T("1--.", "---A", ">---", "GET_STATE"): return
        if self.T("1--A", "---B", ">---", "GET_STATE"): return
        if self.T("1--B", "---C", ">---", "GET_STATE"): return
        if self.T("1--C", "---D", ">---", "GET_STATE"): return
        if self.T("1--D", "---E", ">---", "GET_STATE"): return
        if self.T("1--E", "---F", ">---", "GET_STATE"): return
        if self.T("1--F", "---G", ">---", "GET_STATE"): return
        if self.T("1--G", "---H", ">---", "GET_STATE"): return
        if self.T("1--H", "----", "----", "REJECT"): return

        if self.T("0--A", "--A-", "->->", "REWIND"): return
        if self.T("0--B", "--B-", "->->", "REWIND"): return
        if self.T("0--C", "--C-", "->->", "REWIND"): return
        if self.T("0--D", "--D-", "->->", "REWIND"): return
        if self.T("0--E", "--E-", "->->", "REWIND"): return
        if self.T("0--F", "--F-", "->->", "REWIND"): return
        if self.T("0--G", "--G-", "->->", "REWIND"): return
        if self.T("0--H", "--H-", "->->", "REWIND"): return

    def NEXT_STATE(self):
        if self.T("1---", "---.", ">---", "NEXT_STATE"): return
        if self.T("0--.", "---0", ">---", "NEXT_STATE"): return
        if self.T("0--0", "----", ">-->", "SCAN_STATE"): return

    def HALT(self):
        if self.T("1---", "---.", ">---", "HALT"): return
        if self.T("0--.", "---A", ">---", "HALT"): return
        if self.T("0--A", "---B", ">---", "HALT"): return
        if self.T("0--B", "---.", ">---", "SCAN_FINAL"): return


    def run(self):
        """Executes the turing machine"""
        counter = 0

        import time, os

        while True:
            if str(self.tape(0)) == '.':
                raise ValueError("Invalid Symbol")

            self._steps += 1
            os.system('clear')
            print(self)
            time.sleep(0.01)

            if self._state == "REWIND":
                self.REWIND()
            elif self._state == "START":
                self.START()
            elif self._state == "SCAN_STATE":
                self.SCAN_STATE()
            elif self._state == "SCAN_INPUT":
                self.SCAN_INPUT()
            elif self._state == "SCAN_FINAL":
                self.SCAN_FINAL()
            elif self._state == "CHECK_STATE":
                self.CHECK_STATE()
            elif self._state == "CHECK_INPUT":
                self.CHECK_INPUT()
            elif self._state == "CHECK_FINAL":
                self.CHECK_FINAL()
            elif self._state == "GET_STATE":
                self.GET_STATE()
            elif self._state == "NEXT_STATE":
                self.NEXT_STATE()
            elif self._state == "HALT":
                self.HALT()
            elif self.state == "ACCEPT":
                print('\033[93mSteps\033[0m:', self._steps, '\n')
                return True
            elif self.state == "REJECT":
                print('\033[93mSteps\033[0m:', self._steps, '\n')
                return False
            else:
                raise ValueError("Invalid State")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(f"ERROR: {sys.argv[0]} <input_string>")

    TM(f'{F_DFA}#{sys.argv[1]}').run()

