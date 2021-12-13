from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple, List, Set


@dataclass
class Cave:
    name: str

    def is_start(self):
        return self.name == 'start'

    def is_end(self):
        return self.name == 'end'

    def is_big_cave(self):
        return self.name.isupper()

    def is_small_cave(self):
        return self.name.islower() and not self.is_start() and not self.is_end()

    def __repr__(self):
        return f'Cave({self.name})'

    def __hash__(self) -> int:
        return hash(self.name)


CAVE_PATH = Tuple[Cave, ...]


class CaveMap:
    def __init__(self, cave_connections: List[Tuple[Cave, Cave]]):
        neighbors = defaultdict(set)
        for cave1, cave2 in cave_connections:
            neighbors[cave1].add(cave2)
            neighbors[cave2].add(cave1)
        self._neighbors = dict(neighbors)

    def get_neighbors_of(self, cave: Cave) -> Set[Cave]:
        return self._neighbors[cave]

    def build_path(self, visited_caves: CAVE_PATH, allowance_to_visit_small_cave_twice: bool = False) -> Set[CAVE_PATH]:
        current_cave = visited_caves[-1]
        if current_cave.is_start() and visited_caves.count(current_cave) > 1:
            return set()

        visitation_count = visited_caves.count(current_cave)
        if current_cave.is_small_cave() and visitation_count > 1:
            if allowance_to_visit_small_cave_twice is False:
                return set()
            else:
                allowance_to_visit_small_cave_twice = False

        if current_cave.is_end():
            return {visited_caves}

        return set.union(
            *(self.build_path(visited_caves + (neighbor,), allowance_to_visit_small_cave_twice)
              for neighbor in self.get_neighbors_of(current_cave))
        )

    def __str__(self):
        return '\n'.join(f'{cave} -> {neighbors}' for cave, neighbors in self._neighbors.items())


def main():
    lines = open("input.txt").readlines()
    cave_map = CaveMap([
        tuple(map(Cave, line.rstrip().split('-')))
        for line in lines
    ])

    start_cave = Cave('start')
    part_1_nr_paths = len(cave_map.build_path((start_cave, ), allowance_to_visit_small_cave_twice=False))
    part_2_nr_paths = len(cave_map.build_path((start_cave, ), allowance_to_visit_small_cave_twice=True))
    print(part_1_nr_paths, part_2_nr_paths)


if __name__ == '__main__':
    main()
