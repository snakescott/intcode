from intcode.vm import Computer
from intcode.vm import OpCode


def test_simple():
    memory = [1002, 4, 3, 4, 33]
    c = Computer(memory)
    assert c.opcode == OpCode.MULT
    assert c.src_arg_value(0) == 33
    assert c.src_arg_value(1) == 3
    assert c.dst_arg_value(2) == 4
    assert c.opcode.width == 4

    c.pc += 4
    c.memory[c.pc] = 99
    assert c.opcode == OpCode.HALT


def test_execute():
    memory = [1002, 4, 3, 4, 33]
    c = Computer(memory)
    count = c.run()
    assert memory == [1002, 4, 3, 4, 99]
    assert count == 1


def test_max_count():
    memory = [1002, 4, 3, 4, 33]
    c = Computer(memory)
    count = c.run(max_count=0)
    assert memory == [1002, 4, 3, 4, 33]
    assert count == 0


def test_new_instructions():
    memory = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    c = Computer(memory)
    c.insert_input(7)
    c.run(max_count=100)
    assert c.peek_output() == 0
