from __future__ import annotations

from typing import Tuple, Set, Optional


DOT = Tuple[int, int]


class TransparentPaper:
    def __init__(self, dots: Set[DOT], width: Optional[int] = None, height: Optional[int] = None):
        self._dots = frozenset(dots)
        self.width: int = width if width else max(x for (x, y) in self._dots)
        self.height: int = height if height else max(y for (x, y) in self._dots)

    def count_dots(self) -> int:
        return len(self._dots)

    def fold_x_axis(self, x_axis: int) -> TransparentPaper:
        dots: Set[DOT] = set()
        for (x, y) in self._dots:
            if x < x_axis:
                dots.add((x, y))
            elif x == x_axis:
                # a dot on the folding axis will disappear
                # (though this should never happen according to puzzle instructions)
                pass
            elif x > x_axis:
                x_diff = x - x_axis
                dots.add((x_axis - x_diff, y))

        if any(x < 0 for (x, y) in dots):
            raise ValueError("Paper folded so that points are left of x=0 line")

        return TransparentPaper(dots, width=x_axis)

    def fold_y_axis(self, y_axis: int) -> TransparentPaper:
        dots: Set[DOT] = set()
        for (x, y) in self._dots:
            if y < y_axis:
                dots.add((x, y))
            elif y == y_axis:
                # a dot on the folding axis will disappear
                # (though this should never happen according to puzzle instructions)
                pass
            elif y > y_axis:
                y_diff = y - y_axis
                dots.add((x, y_axis - y_diff))

        if any(y < 0 for (x, y) in dots):
            raise ValueError("Paper folded so that points are above y=0 line")

        return TransparentPaper(dots, height=y_axis)

    def __str__(self):
        output = ""
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                output += "#" if (x, y) in self._dots else " "
            output += "\n"

        return output


def main():
    input_dots, input_folds = open("input.txt").read().split('\n\n')
    dots = {tuple(map(int, line.split(','))) for line in input_dots.split('\n')}
    transparent_paper = TransparentPaper(dots)

    for i, line in enumerate(input_folds.rstrip().split('\n')):
        assert line.startswith('fold along ')
        folding_line = line.split()[-1]
        axis, number = folding_line.split('=')
        if axis == 'x':
            transparent_paper = transparent_paper.fold_x_axis(int(number))
        elif axis == 'y':
            transparent_paper = transparent_paper.fold_y_axis(int(number))
        else:
            raise ValueError(f"Unrecognised folding instructions: '{line}'")

        if i == 0:
            print(transparent_paper.count_dots())

    print(transparent_paper)


if __name__ == '__main__':
    main()
