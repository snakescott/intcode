import operator
from enum import Enum
from functools import partial
from sys import maxsize


def _cmp(fn, c):
    dest = c.dst_arg_value(2)
    if fn(c.src_arg_value(0), c.src_arg_value(1)):
        c.memory[dest] = 1
    else:
        c.memory[dest] = 0


def _binop(fn, c):
    dest = c.dst_arg_value(2)
    value = fn(c.src_arg_value(0), c.src_arg_value(1))
    c.memory[dest] = value


def _jmp_if(fn, c):
    test_value = c.src_arg_value(0)
    if fn(test_value):
        c.pc = c.src_arg_value(1)


def _input(c):
    dest = c.dst_arg_value(0)
    c.memory[dest] = c.pop_input()


def _output(c):
    value = c.src_arg_value(0)
    c.insert_output(value)


class OpCode(Enum):
    ADD = (1, 4, partial(_binop, operator.add))
    MULT = (2, 4, partial(_binop, operator.mul))
    INPUT = (3, 2, _input)
    OUTPUT = (4, 2, _output)
    JT = (5, 3, partial(_jmp_if, lambda x: x != 0))
    JF = (6, 3, partial(_jmp_if, lambda x: x == 0))
    LT = (7, 4, partial(_cmp, operator.lt))
    EQ = (8, 4, partial(_cmp, operator.eq))
    HALT = (99, 1, None)

    def __init__(self, code, width, fn):
        self.code = code
        self.width = width
        self.fn = fn

    @staticmethod
    def from_code(code):
        for op_code in OpCode:
            if op_code.code == code:
                return op_code
        raise ValueError('Unknown OpCode {code}')


class Computer:
    def __init__(self, memory, output_tap=None):
        self._input = []
        self._output = []
        self.output_tap = output_tap
        self.pc = 0
        self.memory = memory

    def insert_input(self, input_):
        self._input.insert(0, input_)

    def pop_input(self):
        return self._input.pop()

    def insert_output(self, output_):
        self._output.insert(0, output_)
        if self.output_tap is not None:
            self.output_tap.append(output_)

    def peek_output(self):
        return self._output[0]

    @property
    def has_input(self):
        return len(self._input) > 0

    @property
    def is_halted(self):
        return self.opcode == OpCode.HALT

    @property
    def is_blocked(self):
        return self.opcode == OpCode.INPUT and not self.has_input

    @property
    def instruction(self):
        return self.memory[self.pc]

    @property
    def opcode(self):
        return OpCode.from_code(self.memory[self.pc] % 100)

    def _raw_value(self, arg_num):
        return self.memory[self.pc + arg_num + 1]

    def src_arg_value(self, arg_num):
        return self._value(arg_num)

    def dst_arg_value(self, arg_num):
        return self._raw_value(arg_num)

    def _value(self, arg_num):
        immediate_idx = 10 ** (2 + arg_num)
        immediate = (self.instruction // immediate_idx) % 10
        if immediate > 1:
            raise ValueError(f'Unexpected value of immediate for {arg_num} of instruction {self.opcode}')

        if immediate:
            return self._raw_value(arg_num)
        else:
            value_index = self._raw_value(arg_num)
            return self.memory[value_index]

    def _execute(self):
        old_pc = self.pc
        if self.opcode == OpCode.HALT:
            raise ValueError('Should never execute a HALT')

        self.opcode.fn(self)
        if old_pc == self.pc:
            self.pc += self.opcode.width

    def run(self, max_count=maxsize):
        count = 0
        while count < max_count and not (self.is_halted or self.is_blocked):
            self._execute()
            count += 1
        return count
