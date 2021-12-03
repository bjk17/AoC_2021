#!/usr/bin/env python

lines = open("input.txt").read().splitlines()

# assuming all lines are of the same length and contains only zeros and ones
nr_of_lines = len(lines)
line_length = len(lines[0])

column_sums = [0] * line_length
for line in lines:
    for i, b in enumerate(line):
        column_sums[i] += int(b)

gamma, epsilon = 0, 0
for i, cs in enumerate(reversed(column_sums)):
    if cs > nr_of_lines/2:
        gamma += 2**i
    elif cs < nr_of_lines/2:
        epsilon += 2**i
    else:
        raise ValueError(f"Each column should either have clearly more 1's or 0's")

print(gamma * epsilon)
