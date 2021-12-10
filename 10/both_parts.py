from typing import Tuple, Optional
from statistics import median

opening_chars = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

closing_chars = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}

corruption_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

autocompletion_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def calculate_line_score(line: str) -> Tuple[Optional[int], Optional[int]]:
    stack = list()
    for char in line.rstrip():
        if char in opening_chars:
            stack.append(char)
        elif char in closing_chars:
            corresponding_opening_char = closing_chars[char]
            if corresponding_opening_char != stack.pop():
                return corruption_scores[char], None

    autocompletion_score = 0
    while len(stack) > 0:
        opening_char = stack.pop()
        closing_char = opening_chars[opening_char]
        closing_char_score = autocompletion_scores[closing_char]
        autocompletion_score = autocompletion_score * 5 + closing_char_score

    return None, autocompletion_score


def main():
    lines = open("input.txt").readlines()

    part_1_corruption_score = 0
    part_2_autocompletion_score = list()
    for line in lines:
        corruption_score, autocompletion_score = calculate_line_score(line)
        if corruption_score:
            part_1_corruption_score += corruption_score
        if autocompletion_score:
            part_2_autocompletion_score.append(autocompletion_score)

    print(part_1_corruption_score, int(median(part_2_autocompletion_score)))


if __name__ == '__main__':
    main()
