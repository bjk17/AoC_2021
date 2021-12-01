#!/usr/bin/env python

lines = open("input.txt").read().split()

first = int(lines[0])
second = int(lines[1])
third = int(lines[2])

increases = 0
previous_measurement = first + second + third

for line in lines[3:]:
    first = second
    second = third
    third = int(line)

    next_measurement = first + second + third
    if next_measurement > previous_measurement:
        increases += 1

    previous_measurement = next_measurement

print(increases)