#!/usr/bin/env python

lines = open("input.txt").readlines()

depth, horizontal_position = 0, 0
for line in lines:
    action, qty = line.split()
    qty = int(qty)

    if action == 'forward':
        horizontal_position += qty
    elif action == 'down':
        depth += qty
    elif action == 'up':
        depth -= qty
    else:
        raise ValueError(f"Action '{action}' in line '{line}' not understood")

print(depth * horizontal_position)
