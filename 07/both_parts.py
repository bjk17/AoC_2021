from math import ceil, fabs, floor
from statistics import mean, median
from typing import List


def linear_cost(crabs_horizontal_positions: List[int], moving_to_position: int) -> int:
    return sum(int(fabs(moving_to_position - horizontal_position)) for horizontal_position in crabs_horizontal_positions)


def ladder_cost(crabs_horizontal_positions: List[int], moving_to_position: int) -> int:
    def ladder_cost_of_moving_between(a: int, b: int) -> int:
        diff = int(fabs(a - b))
        return diff * (diff + 1) // 2

    return sum(ladder_cost_of_moving_between(moving_to_position, horizontal_position) for horizontal_position in crabs_horizontal_positions)


lines = open("input.txt").readlines()
horizontal_positions = list(map(int, lines[0].split(',')))

# best position is somewhere where equally many crabs move to the left and right
median_position = int(round(median(horizontal_positions)))
part_1_fuel_cost = linear_cost(horizontal_positions, median_position)

# according to my calculations the best position is somewhere
# in the interval [mean - 1/2, mean + 1/2]
mean_position = mean(horizontal_positions)
interval = range(floor(mean_position - 1/2), ceil(mean_position + 1/2) + 1)
part_2_fuel_cost = min(ladder_cost(horizontal_positions, position) for position in interval)

print(part_1_fuel_cost, part_2_fuel_cost)
