from collections import Counter

lines = open("input.txt").readlines()
list_of_ages = list(map(int, lines[0].split(',')))


def number_of_fishes_after(days: int) -> int:
    # counting the number of fishes (values) by internal timer state (key)
    lantern_fishes = Counter(list_of_ages)

    for day in range(days):
        new_offsprings = lantern_fishes[0]

        # internal timer decreases by one each day
        for i in range(8):
            lantern_fishes[i] = lantern_fishes[i + 1]

        # the fishes that cloned themselves have their internal timer set to 6
        lantern_fishes[6] += new_offsprings

        # the newly cloned fishes start with a higher timer of 8
        lantern_fishes[8] = new_offsprings

    # in Python 3.10: lantern_fishes.total()
    return sum(lantern_fishes.values())


print(number_of_fishes_after(80))
print(number_of_fishes_after(256))
