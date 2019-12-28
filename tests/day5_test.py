from intcode.test import load_int
from intcode.test import load_memory
from intcode.vm import Computer


def test_day5a():
    input_ = load_memory('day5.input')
    output_ = load_int('day5a.output')

    c = Computer(input_)
    c.insert_input(1)
    count = c.run(max_count=1000)
    assert count == 61
    assert c.peek_output() == output_


def test_day5b():
    input_ = load_memory('day5.input')
    output_ = load_int('day5b.output')

    c = Computer(input_)
    c.insert_input(5)
    count = c.run(max_count=1000)
    assert count == 103
    assert c.peek_output() == output_
