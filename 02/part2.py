#!/usr/bin/env python

lines = open("input.txt").readlines()

aim, depth, horizontal_position = 0, 0, 0
for line in lines:
    action, qty = line.split()
    qty = int(qty)

    if action == 'forward':
        horizontal_position += qty
        depth += aim * qty
    elif action == 'down':
        aim += qty
    elif action == 'up':
        aim -= qty
    else:
        raise ValueError(f"Action '{action}' in line '{line}' not understood")

print(depth * horizontal_position)
