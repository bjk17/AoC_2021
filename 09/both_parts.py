from typing import FrozenSet, Set, Tuple
import math

POINT = Tuple[int, int]


class HeightMap:
    def __init__(self, heightmap: Tuple[Tuple[int]]):
        row_lengths = {len(row) for row in heightmap}
        if not len(row_lengths) == 1:
            raise ValueError("All rows if input 'heightmap' must be of same length")

        self.nr_rows = len(heightmap)
        self.nr_columns = row_lengths.pop()
        self._heightmap = heightmap

    def height_at_point(self, point: POINT) -> int:
        r, c = point
        return self._heightmap[r][c]

    def neighbors_of_point(self, point: POINT) -> Set[POINT]:
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

    def get_low_points(self) -> Set[POINT]:
        low_points = set()
        for r in range(self.nr_rows):
            for c in range(self.nr_columns):
                height_of_point = self.height_at_point((r, c))
                adjacent_locations = self.neighbors_of_point((r, c))

                if all(height_of_point < self.height_at_point(point) for point in adjacent_locations):
                    low_points.add((r, c))

        return low_points

    def expand_basin(self, expand_with: Set[POINT], already_part_of_the_basin: Set[POINT]) -> FrozenSet[POINT]:
        if not expand_with:
            return frozenset(already_part_of_the_basin)

        neighbors = set()
        for point in expand_with:
            height_of_point = self.height_at_point(point)

            neighbors_of_point = self.neighbors_of_point(point) - expand_with - already_part_of_the_basin
            if height_of_point < 9 and all(height_of_point <= self.height_at_point(_point) for _point in neighbors_of_point):
                already_part_of_the_basin.add(point)
                neighbors.update(neighbors_of_point)

        return self.expand_basin(expand_with=neighbors, already_part_of_the_basin=already_part_of_the_basin)


def main():
    lines = open("input.txt").readlines()
    heightmap = HeightMap(tuple(
        tuple(map(int, row.rstrip()))
        for row in lines
    ))

    low_points = heightmap.get_low_points()
    risk_level = sum(heightmap.height_at_point(point) + 1 for point in low_points)
    print(risk_level)

    basins = set()
    for low_point in low_points:
        basin = heightmap.expand_basin(expand_with={low_point}, already_part_of_the_basin=set())
        basins.add(basin)

    basin_lengths = [len(basin) for basin in basins]
    top_three_basin_sizes_multiplied_together = math.prod(sorted(basin_lengths, reverse=True)[:3])
    print(top_three_basin_sizes_multiplied_together)


if __name__ == '__main__':
    main()