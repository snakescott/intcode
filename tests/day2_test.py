from itertools import product

from intcode.test import load_int
from intcode.test import load_memory
from intcode.vm import Computer


def test_day2a():
    input_ = load_memory('day2.input')
    output_ = load_int('day2a.output')

    input_[1:3] = [12, 2]
    c = Computer(input_)
    c.run()
    assert c.memory[0] == output_


def test_day2b():
    input_ = load_memory('day2.input')
    output_ = load_int('day2b.output')

    for (noun, verb) in product(range(0, 100), range(0, 100)):
        data = list(input_)
        data[1:3] = [noun, verb]
        c = Computer(data)
        c.run()
        if c.memory[0] == 19690720:
            break
    assert noun * 100 + verb == output_
