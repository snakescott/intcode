from enum import Enum
from itertools import permutations
from sys import maxsize

from intcode.vm import Computer


def thrust(phases, memory, max_count=maxsize):
    amps = [Computer(list(memory)) for phase in phases]
    for (amp, phase) in zip(amps, phases):
        amp.insert_input(phase)

    output = 0
    for amp in amps:
        amp.insert_input(output)
        amp.run(max_count=max_count)
        output = amp.peek_output()

    return output


def turbo_thrust(phases, memory, max_count=maxsize, max_loops=1000):
    amps = [Computer(list(memory)) for phase in phases]
    for idx in range(len(amps)):
        amp = amps[idx]
        next_amp = amps[(idx + 1) % len(amps)]
        amp._output = next_amp._input

    for (amp, phase) in zip(amps, phases):
        amp.insert_input(phase)

    amps[-1].output_tap = []
    amps[0].insert_input(0)

    for loop in range(max_loops):
        halted = 0
        for amp in amps:
            amp.run(max_count=max_count)
            if amp.is_halted:
                halted += 1
        if halted == len(amps):
            break

    return amps[-1].output_tap[-1]


class ThrustType(Enum):
    STANDARD = (thrust, list(permutations([0, 1, 2, 3, 4])))
    TURBO = (turbo_thrust, list(permutations([5, 6, 7, 8, 9])))

    def __init__(self, thrust_fn, all_phases):
        self.thrust_fn = thrust_fn
        self.all_phases = all_phases

    def max(self, memory, **kwargs):
        return max(self.thrust_fn(p, memory, **kwargs) for p in self.all_phases)
