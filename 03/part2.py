#!/usr/bin/env python
from typing import Set


def most_common_bit(bitstrings: Set[str], bit_index: int) -> int:
    column_sum = sum(int(bitstring[bit_index]) for bitstring in bitstrings)
    return 1 if column_sum >= len(bitstrings)/2 else 0


def least_common_bit(bitstrings: Set[str], bit_index: int) -> int:
    column_sum = sum(int(bitstring[bit_index]) for bitstring in bitstrings)
    return 1 if column_sum < len(bitstrings)/2 else 0


def calculate(bitstring: str) -> int:
    return sum(2**i if b == '1' else 0 for i, b in enumerate(reversed(bitstring)))


lines = open("input.txt").read().splitlines()

# assuming all lines are of the same length and contains only zeros and ones
nr_of_lines = len(lines)
line_length = len(lines[0])

oxygen_score = 0
oxygen_numbers = set(lines)
for i in range(line_length):
    bit = most_common_bit(oxygen_numbers, i)
    oxygen_numbers = {number for number in oxygen_numbers if int(number[i]) == bit}
    if len(oxygen_numbers) == 1:
        oxygen_score = calculate(oxygen_numbers.pop())
        break

co2_scrubber_score = 0
co2_scrubber_numbers = set(lines)
for i in range(line_length):
    bit = least_common_bit(co2_scrubber_numbers, i)
    co2_scrubber_numbers = {number for number in co2_scrubber_numbers if int(number[i]) == bit}

    if len(co2_scrubber_numbers) == 1:
        co2_scrubber_score = calculate(co2_scrubber_numbers.pop())
        break

print(oxygen_score * co2_scrubber_score)