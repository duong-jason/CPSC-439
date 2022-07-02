#!/usr/bin/env python3


import sys
import time, os
from encode import *


class TM:
    def __init__(self, input_string):
        self._tape = list(map(lambda x: list('▷' + x), [input_string, BLANK, R1, BLANK]))
        self._head = [0] * TAPE_LEN
        self._state = 'SETUP_TAPE'
        self._move = STAY
        self._steps = 0


        # FIX
        self._delta = {
            "SETUP_TAPE": self.SETUP_TAPE,
            "REWIND_STATE": self.REWIND_STATE,
            "REWIND_INPUT": self.REWIND_INPUT,
            "COPY_INPUT": self.COPY_INPUT,
            "START": self.START,
            "SCAN_STATE": self.SCAN_STATE,
            "SCAN_INPUT": self.SCAN_INPUT,
            "SCAN_FINAL": self.SCAN_FINAL,
            "CHECK_STATE": self.CHECK_STATE,
            "CHECK_INPUT": self.CHECK_INPUT,
            "CHECK_FINAL": self.CHECK_FINAL,
            "GET_STATE": self.GET_STATE,
            "NEXT_STATE": self.NEXT_STATE,
            "GOTO_FINAL": self.GOTO_FINAL,
            "ACCEPT": self.ACCEPT,
            "REJECT": self.REJECT
        }


    def __str__(self):
        '''Outputs the current tape state'''
        # FIX
        res = ''
        print('\033[32m' + self._state + '\033[0m')

        if SHOW_HEAD:
            for i in range(TAPE_LEN):
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
            for i in range(TAPE_LEN):
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

    def __getitem__(self, pos):
        '''Returns the symbol on a particular tape'''
        if pos > TAPE_LEN:
            raise IndexError(pos)
        return self._tape[pos][self._head[pos]]


    def __setitem__(self, pos, symbol):
        """Writes a symbol on each tape"""
        self._tape[pos][self._head[pos]] = symbol


    @property
    def state(self):
        return self._state


    @state.setter
    def state(self, state):
        self._state = state

    @property
    def move(self):
        return self._move


    @move.setter
    def move(self, move):
        self._move = move 

    def symbol(self, action):
        symbol = [self[i] for i in range(TAPE_LEN)]
        [symbol.pop(i) and action.pop(i) for i in reversed(range(TAPE_LEN)) if action[i] == STAY]
        return symbol == action


    def move(self):
        """Moves the head position on each tape"""
        for i, move in enumerate(self._move):
            if move == LEFT:
                self._head[i] = max(0, self._head[i] - 1)
            elif move == RIGHT:
                if self._head[i] >= len(self._tape[i]) - 1:
                    self._tape[i].append(BLANK)
                self._head[i] += 1
            elif move == STAY:
                pass
            else:
                raise ValueError


    def T(self, x, y, z, i):
        x, y, z = map(lambda f: list(f), [x, y, z])

        if self[2] not in list(f'{START}.ABCDEFGH'):
                exit()

        for index, k in enumerate(x):
            if k == "*":
                print(x[index])
                x[index] = self[index]
                print(x[index])
                for index1, p in enumerate(y):
                    if p == "*":
                        y[index1] = x[index]
                    elif p == "+":
                        print(x[index])
                        match x[index]:
                            case '.': y[index1] = "A"
                            case 'A': y[index1] = "B"
                            case 'B': y[index1] = "C"
                            case 'C': y[index1] = "D"
                            case 'D': y[index1] = "E"
                            case 'E': y[index1] = "G"
                            case 'G': y[index1] = "H"
            if k == "!":
                for r in range(index + 1, len(x)):
                    if x[r] == "!":
                        if self[index] == self[r]:
                            for q in range(TAPE_LEN):
                                if y[q] != STAY:
                                    self[q] = y[q]
                            self._move = z
                            self.move()
                            self.state = i
                            return True
        """
        if COPY in x:
            xpos = x.index(COPY)
            x[xpos] = self[xpos]
            print(xpos, xpos)
            if COPY in y:
                ypos = y.index(COPY)
                y[ypos] = self[xpos]
            elif INCR in y:
                rule = '.ABCDEFGH'
                ypos = y.index(INCR)
                y[ypos] = rule[min(rule.find(self[ypos]) + 1, len(rule))]
        if EQ in x:
            if all(self[r] for r in [k for k in range(TAPE_LEN) if x[k] == EQ]):
                for q in range(TAPE_LEN):
                    if y[q] != STAY:
                        self[q] = y[q]
                    self._move = z
                    self.move()
                    self.state = i
                    return True
        """

        if self.symbol(x):
            for q in range(TAPE_LEN):
                if y[q] != STAY:
                    self[q] = y[q]
            self._move = z
            self.move()
            self.state = i
            return True
        return False


    def SETUP_TAPE(self):
        if self.T("#---", ".---", ">>--", "COPY_INPUT"): return
        if self.T("----", "----", ">---", "SETUP_TAPE"): return


    def COPY_INPUT(self):
        if self.T("0---", ".0--", ">>--", "COPY_INPUT"): return
        if self.T("1---", ".1--", ">>--", "COPY_INPUT"): return
        if self.T(".---", "----", "----", "REWIND_INPUT"): return


    def REWIND_INPUT(self):
        if self.T("-▷--", "----", "----", "REWIND_STATE"): return
        if self.T("----", "----", "-<--", "REWIND_INPUT"): return


    def REWIND_STATE(self):
        if self.T("▷---", "----", "----", "START"): return
        if self.T("----", "----", "<---", "REWIND_STATE"): return


    def START(self):
        if self.T("▷▷▷▷", "----", ">>>>", "SCAN_STATE"): return
        if self.T("▷.--", "----", ">---", "GOTO_FINAL"): return
        if self.T("▷---", "----", ">---", "SCAN_STATE"): return

    def SCAN_STATE(self):
        if self.T("-.--", "----", ">---", "GOTO_FINAL"): return # note: empty string input
        if self.T("1--*", "---+", ">---", "SCAN_STATE"): return
        if self.T("1--H", "----", "----", "REJECT"): return
        if self.T("0---", "----", ">---", "CHECK_STATE"): return

    def SCAN_INPUT(self):
        if self.T("1--.", "---0", ">---", "SCAN_INPUT"): return
        if self.T("1--0", "---1", ">---", "SCAN_INPUT"): return
        if self.T("1--1", "----", "----", "REJECT"): return
        if self.T("0---", "----", ">---", "CHECK_INPUT"): return

    def SCAN_FINAL(self):
        if self.T("1--#", "----", "--->", "SCAN_FINAL"): return
        if self.T("1--*", "---+", ">---", "SCAN_FINAL"): return
        if self.T("0---", "----", ">-->", "SCAN_FINAL"): return
        if self.T(".--#", "----", "----", "REJECT"): return
        if self.T(".---", "----", "---<", "CHECK_FINAL"): return

    def CHECK_STATE(self):
        if self.T("--!!", "----", "--->", "SCAN_INPUT"): return
        if self.T("----", "----", "--->", "NEXT_STATE"): return

    def CHECK_INPUT(self):
        if self.T("-!-!", "----", "-->>", "GET_STATE"): return
        if self.T("----", "----", "--->", "NEXT_STATE"): return

    def CHECK_FINAL(self):
        if self.T("--!!", "----", "----", "ACCEPT"): return
        if self.T("---#", "----", "----", "REJECT"): return
        if self.T("----", "----", "---<", "CHECK_FINAL"): return

    def GET_STATE(self):
        if self.T("1--*", "---+", ">---", "GET_STATE"): return
        if self.T("1--H", "----", "----", "REJECT"): return
        if self.T("0--*", "--*-", "->->", "REWIND_STATE"): exit()

    def NEXT_STATE(self):
        if self.T("1---", "---.", ">---", "NEXT_STATE"): return
        if self.T("0--.", "---0", ">---", "NEXT_STATE"): return
        if self.T("0--0", "----", ">-->", "SCAN_STATE"): return
        if self.T("----", "----", "----", "REJECT"): return

    def GOTO_FINAL(self):
        if self.T("1---", "---.", ">---", "GOTO_FINAL"): return
        if self.T("0--B", "---#", ">---", "SCAN_FINAL"): return
        if self.T("0--*", "---+", ">---", "GOTO_FINAL"): return

    def ACCEPT(self):
        raise HaltProcess("ACCEPT")

    def REJECT(self):
        raise HaltProcess("REJECT")

    def run(self):
        """Executes the turing machine"""
        while True:
            try:
                os.system('clear')
                print(self)
                time.sleep(MEDIUM)


                self._delta[self._state]()
                self._steps += 1
            except KeyError:
                return f"Invalid State: {self._state}"
            except ValueError:
                return f"Invalid Move: {self._move}"
            except IndexError as pos:
                return f"Invalid Cell: {pos}"
            except HaltProcess:
                return f"\033[93mSteps\033[0m: {self._steps}\n"


if __name__ == '__main__':
    if len(sys.argv) != 2:
     exit(f"ERROR: {sys.argv[0]} <input_string>")

    XOR_TM = TM(f'{TEST}{SEP}{sys.argv[1]}')
    print(XOR_TM.run())
