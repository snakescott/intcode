from itertools import product

from intcode.test import resource_string
from intcode.vm import Computer


def test_day2a():
    input_ = resource_string('day2.input')
    output_ = resource_string('day2a.output')

    input_ = list(map(int, input_.strip().split(',')))
    input_[1:3] = [12, 2]
    output_ = int(output_.strip())

    c = Computer(input_)
    c.run()
    assert c.memory[0] == output_


def test_day2b():
    input_ = resource_string('day2.input')
    output_ = resource_string('day2b.output')

    input_ = list(map(int, input_.strip().split(',')))
    output_ = int(output_.strip())

    for (noun, verb) in product(range(0, 100), range(0, 100)):
        data = list(input_)
        data[1:3] = [noun, verb]
        c = Computer(data)
        c.run()
        if c.memory[0] == 19690720:
            break
    assert noun * 100 + verb == output_
