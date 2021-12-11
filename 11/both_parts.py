from typing import Tuple, Iterator, List, Set

POINT = Tuple[int, int]


class OctopusArrangement:
    def __init__(self, octopus_energy_levels: List[List[int]]):
        column_widths = {len(row) for row in octopus_energy_levels}
        if not len(column_widths) == 1:
            raise ValueError("All rows if input 'octopus_energy_levels' must be of same length")

        self.nr_rows = len(octopus_energy_levels)
        self.nr_columns = column_widths.pop()
        self._energy_levels = octopus_energy_levels

    def get_octopus_count(self) -> int:
        return self.nr_rows * self.nr_columns

    def get_all_points(self) -> Iterator[POINT]:
        for r in range(self.nr_rows):
            for c in range(self.nr_columns):
                yield r, c

    def neighbors_of(self, point: POINT) -> Set[POINT]:
        r, c = point
        neighbors = set()

        left_of_point: bool = c > 0
        right_of_point: bool = c < self.nr_columns - 1
        above_point: bool = r > 0
        below_point: bool = r < self.nr_rows - 1

        if above_point:
            neighbors.add((r - 1, c))
        if below_point:
            neighbors.add((r + 1, c))

        if left_of_point:
            neighbors.add((r, c - 1))
        if right_of_point:
            neighbors.add((r, c + 1))

        if right_of_point and above_point:
            neighbors.add((r - 1, c + 1))
        if right_of_point and below_point:
            neighbors.add((r + 1, c + 1))
        if left_of_point and below_point:
            neighbors.add((r + 1, c - 1))
        if left_of_point and above_point:
            neighbors.add((r - 1, c - 1))

        return neighbors

    def energy_level_at(self, point: POINT) -> int:
        r, c = point
        return self._energy_levels[r][c]

    def reset_energy_at(self, point: POINT) -> None:
        r, c = point
        self._energy_levels[r][c] = 0

    def increase_energy_at(self, point: POINT) -> bool:
        """
        Returns True if this leads to point flashing
        """
        if self.energy_level_at(point) > 9:
            return False

        r, c = point
        self._energy_levels[r][c] += 1
        return self.energy_level_at(point) > 9

    def flash_at(self, point: POINT) -> Set[POINT]:
        """
        Flashes the point, possibly starting a chain reaction of flashes, and returns them all
        """
        flashing_points = {point}
        for neighbor in self.neighbors_of(point):
            if self.increase_energy_at(neighbor):
                flashing_points.update(self.flash_at(neighbor))

        return flashing_points

    def step(self) -> int:
        """
        Returns the number of flashes in this step
        """
        flashing_points = set()
        for point in self.get_all_points():
            if self.increase_energy_at(point):
                flashing_points.update(self.flash_at(point))

        for flashing_point in flashing_points:
            self.reset_energy_at(flashing_point)

        return len(flashing_points)

    def __str__(self) -> str:
        return "\n".join(
            "".join(str(energy_level) for energy_level in row) for row in self._energy_levels
        ) + "\n"


def main():
    lines = open("input.txt").readlines()
    octopus_arrangement = OctopusArrangement(list(
        list(map(int, row.rstrip()))
        for row in lines
    ))

    rounds_done = 0
    cumulative_flashes = 0
    total_flashes_after_100_rounds = None
    first_time_all_flashes = None
    while total_flashes_after_100_rounds is None or first_time_all_flashes is None:
        round_flashes = octopus_arrangement.step()
        cumulative_flashes += round_flashes
        rounds_done += 1

        if rounds_done == 100:
            total_flashes_after_100_rounds = cumulative_flashes

        if first_time_all_flashes is None and round_flashes == octopus_arrangement.get_octopus_count():
            first_time_all_flashes = rounds_done

    print(total_flashes_after_100_rounds, first_time_all_flashes)


if __name__ == '__main__':
    main()
