#!/usr/bin/env python3


import sys
import time, os
from encode import *


class TM:
    def __init__(self, input_string):
        self._tape = list(map(lambda x: list('▷' + x), [input_string, BLANK, REG[0], BLANK]))
        self._head = [0] * TAPE_LEN
        self._state = 'LOAD_TAPE'
        self._move = STAY
        self._steps = 0

        self._delta = {
            "LOAD_TAPE": self.LOAD_TAPE,
            "REWIND_TAPE": self.REWIND_TAPE,
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
        """Outputs the current tape state"""
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
            raise CellFault(pos)
        return self._tape[pos][self._head[pos]]


    def __setitem__(self, pos, symbol):
        """Writes a symbol on each tape"""
        if pos > TAPE_LEN:
            raise CellFault(pos)
        self._tape[pos][self._head[pos]] = symbol


    @property
    def state(self):
        return self._state


    @state.setter
    def state(self, state):
        self._state = state


    @property
    def direction(self):
        return self._move


    @direction.setter
    def direction(self, move):
        self._move = move


    @property
    def steps(self):
        return self._steps


    @steps.setter
    def steps(self, step):
        self._steps = step


    def symbol(self, read):
        head = [self[i] for i in range(TAPE_LEN)]
        [head.pop(i) and read.pop(i) for i in reversed(range(TAPE_LEN)) if read[i] == STAY]
        return head == read


    def write(self, input):
        for i in range(TAPE_LEN):
            if input[i] != STAY:
                self[i] = input[i]


    def move(self, direction):
        """Moves the head position on each tape"""
        self.direction = direction

        for i, move in enumerate(self.direction):
            if move == LEFT:
                self._head[i] = max(0, self._head[i] - 1)
            elif move == RIGHT:
                if self._head[i] >= len(self._tape[i]) - 1:
                    self._tape[i].append(BLANK)
                self._head[i] += 1
            elif move == STAY:
                pass
            else:
                raise MoveError


    def synthesize(self, read, input):
        """Parses the transition symbols"""
        if COPY in read:
            xpos = read.index(COPY)
            read[xpos] = self[xpos]
            if COPY in input:
                ypos = input.index(COPY)
                input[ypos] = self[xpos]
            if INCR in input:
                ypos = input.index(INCR)
                input[ypos] = chr(ord(self[ypos]) + 1)


    def T(self, read, input, direction, next_state):
        """State transition function"""
        read, input, direction = map(lambda f: list(f), [read, input, direction])
        self.synthesize(read, input)

        if EQ in read and all([self[read.index(EQ)] == self[k] for k in range(TAPE_LEN) if read[k] == EQ]) or \
            NEG in read and not all([self[read.index(NEG)] == self[k] for k in range(TAPE_LEN) if read[k] == NEG]) or \
            self.symbol(read):

            self.write(input)
            self.move(direction)
            self.state = next_state
            return True
        return False


    def LOAD_TAPE(self):
        if self.T("#---", ".---", ">>--", "COPY_INPUT"): return
        if self.T("----", "----", ">---", "LOAD_TAPE"): return

    def COPY_INPUT(self):
        if self.T(".---", " ---", "----", "REWIND_INPUT"): return
        if self.T("*---", " *--", ">>--", "COPY_INPUT"): return

    def REWIND_INPUT(self):
        if self.T("-▷--", "----", "----", "REWIND_TAPE"): return
        if self.T("----", "----", "-<--", "REWIND_INPUT"): return

    def REWIND_TAPE(self):
        if self.T("▷---", "----", "----", "START"): return
        if self.T("----", "----", "<---", "REWIND_TAPE"): return

    def START(self):
        if self.T("▷▷▷▷", "----", ">>>>", "SCAN_STATE"): return
        if self.T("▷---", "----", ">---", "SCAN_STATE"): return
        if self.T("-.--", "----", "----", "GOTO_FINAL"): return # note: reached end of input
        if self.T("----", "-❌--", "----", "REJECT"): return

    def SCAN_STATE(self):
        if self.T("-.--", "----", ">---", "GOTO_FINAL"): return # note: empty string input
        if self.T("0---", "----", ">---", "CHECK_STATE"): return
        if self.T("1--Z", "-❌--", "----", "REJECT"): return
        if self.T("1--.", "---A", ">---", "SCAN_STATE"): return
        if self.T("1--*", "---+", ">---", "SCAN_STATE"): return

    def SCAN_INPUT(self):
        if self.T("1--z", "-❌--", "----", "REJECT"): return # note: input not in {a...z}
        if self.T("1--.", "---a", ">---", "SCAN_INPUT"): return
        if self.T("1--*", "---+", ">---", "SCAN_INPUT"): return
        if self.T("0---", "----", ">---", "CHECK_INPUT"): return

    def SCAN_FINAL(self):
        if self.T("1--#", "----", "--->", "SCAN_FINAL"): return # note: marker added to backtrack
        if self.T("0---", "----", ">-->", "SCAN_FINAL"): return
        if self.T("1--Z", "-❌--", "----", "REJECT"): return
        if self.T("1--.", "---A", ">---", "SCAN_FINAL"): return
        if self.T("1--*", "---+", ">---", "SCAN_FINAL"): return
        if self.T(".--#", "-✅--", "----", "ACCEPT"): return     # note: no final states
        if self.T(".---", "----", "---<", "CHECK_FINAL"): return

    def CHECK_STATE(self):
        if self.T("--==", "----", "--->", "SCAN_INPUT"): return
        if self.T("----", "----", "----", "NEXT_STATE"): return

    def CHECK_INPUT(self):
        if self.T("-=-=", "----", "-->>", "GET_STATE"): return
        if self.T("----", "---.", "---<", "NEXT_STATE"): return

    def CHECK_FINAL(self):
        if self.T("--==", "-✅--", "----", "ACCEPT"): return
        if self.T("---#", "-❌--", "----", "REJECT"): return
        if self.T("----", "----", "---<", "CHECK_FINAL"): return

    def NEXT_STATE(self):
        if self.T("1---", "---.", ">---", "NEXT_STATE"): return
        if self.T("0--.", "---#", ">---", "NEXT_STATE"): return
        if self.T("0--#", "---.", ">---", "SCAN_STATE"): return
        if self.T("----", "-❌--", "----", "REJECT"): return

    def GET_STATE(self):
        if self.T("0--*", "--*-", "->->", "REWIND_TAPE"): return
        if self.T("1--Z", "-❌--", "----", "REJECT"): return     # note: state not in {A...Z}
        if self.T("1--.", "---A", ">---", "GET_STATE"): return
        if self.T("1--*", "---+", ">---", "GET_STATE"): return

    def GOTO_FINAL(self):
        if self.T("1---", "---A", ">---", "GOTO_FINAL"): return
        if self.T("0--C", "---#", ">---", "SCAN_FINAL"): return
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
                time.sleep(0.001)

                self._delta[self._state]()
                self._steps += 1
            except KeyError:
                return f"Undefined State: {self.state}"
            except SymbolError as symbol:
                return f"Undefined Symbol: {symbol}"
            except MoveError:
                return f"Undefined Move: {self.direction}"
            except CellFault as index:
                return f"Invalid Cell: {index}"
            except HaltProcess:
                os.system('clear')
                print(self)
                time.sleep(0.001)
                return f"\033[93mSteps\033[0m: {self.steps}\n"


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(f"ERROR: {sys.argv[0]} <input_string>")

    TM(f'{XOR}{SEP}{sys.argv[1]}').run()

