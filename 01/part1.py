#!/usr/bin/env python

lines = open("input.txt").read().split()

increases = 0
previous_measurement = int(lines[0])

for line in lines[1:]:
    next_measurement = int(line)
    if next_measurement > previous_measurement:
        increases += 1

    previous_measurement = next_measurement

print(increases)