from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Set


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Line:
    def __init__(self, p: Point, q: Point):
        self.p = p
        self.q = q
        self.xs = {self.p.x, self.q.x}
        self.ys = {self.p.y, self.q.y}
        self.diff_x = max(self.xs) - min(self.xs)
        self.diff_y = max(self.ys) - min(self.ys)

    def is_vertical(self) -> bool:
        return len(self.xs) == 1

    def is_horizontal(self) -> bool:
        return len(self.ys) == 1

    def is_diagonal(self) -> bool:
        return self.diff_x == self.diff_y

    def get_points(self) -> Set[Point]:
        if self.is_vertical():
            return {Point(self.p.x, y) for y in range(min(self.ys), max(self.ys) + 1)}

        if self.is_horizontal():
            return {Point(x, self.p.y) for x in range(min(self.xs), max(self.xs) + 1)}

        if self.is_diagonal():
            x_step = 1 if q.x > p.x else -1
            y_step = 1 if q.y > p.y else -1
            return {Point(p.x + i * x_step, p.y + i * y_step) for i in range(self.diff_x + 1)}

        return set()

    def __hash__(self) -> int:
        return hash((p, q))


input_lines = open("input.txt").readlines()

counter_part1, counter_part2 = Counter(), Counter()
for input_line in input_lines:
    x1, y1, x2, y2 = map(int, input_line.replace(' -> ', ',').split(','))
    p = Point(x1, y1)
    q = Point(x2, y2)
    line = Line(p, q)

    if line.is_vertical() or line.is_horizontal():
        counter_part1.update(line.get_points())
        counter_part2.update(line.get_points())

    if line.is_diagonal():
        counter_part2.update(line.get_points())

overlap_points_part_1 = sum(count > 1 for count in counter_part1.values())
overlap_points_part_2 = sum(count > 1 for count in counter_part2.values())
print(overlap_points_part_1, overlap_points_part_2)
