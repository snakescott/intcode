from intcode.test import load_int
from intcode.test import load_memory
from intcode.thrust import ThrustType


def test_day7a():
    input_ = load_memory('day7.input')
    output_ = load_int('day7a.output')
    assert ThrustType.STANDARD.max(input_) == output_


def test_day7b():
    input_ = load_memory('day7.input')
    output_ = load_int('day7b.output')
    assert ThrustType.TURBO.max(input_) == output_
