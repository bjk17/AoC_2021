from __future__ import annotations

from typing import Iterator, List, Tuple, Set
import heapq


POINT = Tuple[int, int]


class RiskLevels:
    def __init__(self, risk_levels: Tuple[Tuple[int]]):
        column_widths = {len(row) for row in risk_levels}
        if not len(column_widths) == 1:
            raise ValueError("All rows if input 'risk_levels' must be of same length")

        self.nr_rows = len(risk_levels)
        self.nr_columns = column_widths.pop()

        assert all(risk_levels[c][r] >= 0 for c in range(self.nr_columns) for r in range(self.nr_rows))
        self._risk_levels = risk_levels

    @staticmethod
    def get_top_left() -> POINT:
        return 0, 0

    def get_bottom_right(self) -> POINT:
        return self.nr_rows - 1, self.nr_columns - 1

    def get_all_points(self) -> Iterator[POINT]:
        for r in range(self.nr_rows):
            for c in range(self.nr_columns):
                yield r, c

    def risk_at(self, point) -> int:
        r, c = point
        return self._risk_levels[r][c]

    def neighbors_of(self, point: POINT) -> Set[POINT]:
        r, c = point
        neighbors = set()

        if r > 0:
            neighbors.add((r - 1, c))
        if r < self.nr_rows - 1:
            neighbors.add((r + 1, c))

        if c > 0:
            neighbors.add((r, c - 1))
        if c < self.nr_columns - 1:
            neighbors.add((r, c + 1))

        return neighbors

    def __str__(self) -> str:
        output = ""
        for row in self._risk_levels:
            output += "".join(str(risk) for risk in row) + "\n"

        return output

    def get_lowest_risk(self, start: POINT, end: POINT) -> int:
        # Dijkstra's algorithm

        # for every point 'P' the distance (risk) from 'start' to 'P' is distance[P]
        distance = {start: 0}

        heap_of_lowest_risks = [(0, start)]
        while heap_of_lowest_risks:

            # expand from the point with the lowest risk
            point_distance, point = heapq.heappop(heap_of_lowest_risks)
            if point == end:
                break

            # update risk of neighbors with a possibly shorter path
            for neighbor in self.neighbors_of(point):
                if neighbor not in distance or point_distance + self.risk_at(neighbor) < distance[neighbor]:
                    new_distance = point_distance + self.risk_at(neighbor)
                    distance[neighbor] = new_distance
                    heapq.heappush(heap_of_lowest_risks, (new_distance, neighbor))

        return distance[end]


def increase_values(row: Tuple[int], increase_by: int) -> Tuple[int]:
    return tuple((val - 1 + increase_by) % 9 + 1 for val in row)


def enlarge_risk_levels(risk_levels: Tuple[Tuple[int]], dimension_multiplication: int) -> Tuple[Tuple[int]]:
    rows: List[Tuple[int]] = []

    # enlarge in dimension x (increasing number of columns)
    for row in risk_levels:
        new_row = row
        for c in range(1, dimension_multiplication):
            new_row = new_row + increase_values(row, increase_by=c)

        rows.append(new_row)

    # enlarge in dimension y (increasing number of rows)
    for c in range(1, dimension_multiplication):
        for original_row_count in range(len(risk_levels)):
            row = rows[original_row_count]
            new_row = increase_values(row, increase_by=c)
            rows.append(new_row)

    return tuple(rows)


def main():
    lines = open("input.txt").readlines()
    original_risk_levels = tuple(
        tuple(map(int, row.rstrip()))
        for row in lines
    )

    risk_levels_part_1 = RiskLevels(original_risk_levels)
    print(risk_levels_part_1.get_lowest_risk(risk_levels_part_1.get_top_left(), risk_levels_part_1.get_bottom_right()))

    enlarged_risk_levels = enlarge_risk_levels(original_risk_levels, dimension_multiplication=5)
    risk_levels_part_2 = RiskLevels(enlarged_risk_levels)
    print(risk_levels_part_2.get_lowest_risk(risk_levels_part_2.get_top_left(), risk_levels_part_2.get_bottom_right()))


if __name__ == '__main__':
    main()
