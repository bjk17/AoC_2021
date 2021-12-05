from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Set, Tuple

BINGO_NUMBER = int
BINGO_ROW = Tuple[BINGO_NUMBER, BINGO_NUMBER, BINGO_NUMBER, BINGO_NUMBER, BINGO_NUMBER]
COORDINATES = Tuple[int, int]


class BingoBoard:
    def __init__(self, rows: Tuple[BINGO_ROW, BINGO_ROW, BINGO_ROW, BINGO_ROW, BINGO_ROW]):
        '''
        Representing a 5x5 bingo board with BINGO_NUMBER on each square
        '''
        self.location_of_number: Dict[BINGO_NUMBER, COORDINATES] = dict()
        self.marked: DefaultDict[COORDINATES, bool] = defaultdict(bool)
        self._hash = hash(rows)

        for i, row in enumerate(rows):
            for j, number in enumerate(row):
                coordinates: COORDINATES = (i, j)
                self.location_of_number[number] = coordinates

    def mark_and_score(self, number: BINGO_NUMBER) -> Optional[int]:
        '''
        Marks number 'number' on the bingo board and returns the score (according to AoC) if there is a bingo.
        :param number: a number to be marked which might or might not be on this bingo board
        :return: the score (according to AoC) if this board has a bingo, otherwise None
        '''
        coordinates: Optional[COORDINATES] = self.location_of_number.get(number)
        if not coordinates:
            # the number 'number' isn't on this bingo board
            return None

        self.marked[coordinates] = True
        i, j = coordinates

        # checking if marking (i, j) makes the i'th row or j'th column fully marked -- i.e., a bingo!
        if all(self.marked[(i, k)] for k in range(5)) or all(self.marked[(k, j)] for k in range(5)):
            sum_of_all_unmarked_numbers = sum(
                bingo_number if not self.marked[coordinates] else 0
                for bingo_number, coordinates in self.location_of_number.items()
            )
            return sum_of_all_unmarked_numbers * number

    def __hash__(self):
        return self._hash


def play_bingo(bingo_boards: Set[BingoBoard], bingo_numbers: List[BINGO_NUMBER]) -> Tuple[Optional[int], Optional[int]]:
    winning_score, losing_score = None, None

    bingo_board_scores: Dict[BingoBoard, Optional[int]] = {bingo_board: None for bingo_board in bingo_boards}
    for bingo_number in bingo_numbers:
        for bingo_board in bingo_board_scores.keys():
            bingo_board_scores[bingo_board] = bingo_board.mark_and_score(bingo_number)

        scores = list(bingo_board_scores.values())

        if not losing_score and not any(score is None for score in scores):
            # solving part 2 of problem
            losing_score = min(scores)

        if not winning_score and not all(score is None for score in scores):
            # solving part 1 of problem
            winning_score = max(filter(None, scores))

        # only continuing playing bingo with the boards that haven't had a bingo yet
        bingo_board_scores = {
            bingo_board: score
            for bingo_board, score in bingo_board_scores.items()
            if score is None
        }

    return winning_score, losing_score


lines = open("input.txt").read().split('\n\n')

input_numbers = list(map(int, lines[0].rstrip().split(',')))

bingo_boards: Set[BingoBoard] = set()
for line in lines[1:]:
    bingo_rows = tuple(
        tuple(map(int, row_line.strip().split()))
        for row_line in line.split('\n')
    )
    bingo_board = BingoBoard(bingo_rows)
    bingo_boards.add(bingo_board)

print(play_bingo(bingo_boards, input_numbers))
