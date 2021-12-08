lines = open("input.txt").readlines()

part_1_count, part_2_sum = 0, 0
for line in lines:
    input_side, output_side = line.split(' | ')
    input_segments = list(map(frozenset, input_side.split()))
    output_segments = list(map(frozenset, output_side.split()))

    # len(segment) | possible numbers
    # -------------+--------------------
    #            2 |   1
    #            3 |               7
    #            4 |         4
    #            5 |     2 3   5
    #            6 | 0           6     9
    #            7 |                 8

    digit_to_segment = {}
    for segment in sorted(input_segments, key=len):
        if len(segment) == 2:
            digit_to_segment[1] = segment
        elif len(segment) == 3:
            digit_to_segment[7] = segment
        elif len(segment) == 4:
            digit_to_segment[4] = segment
        elif len(segment) == 7:
            digit_to_segment[8] = segment

    assert sorted(digit_to_segment.keys()) == [1, 4, 7, 8]

    for segment in input_segments:
        if len(segment) == 5 and len(segment - digit_to_segment[1]) == 3:
            digit_to_segment[3] = segment
        elif len(segment) == 6 and len(segment - digit_to_segment[1]) == 5:
            digit_to_segment[6] = segment

    assert sorted(digit_to_segment.keys()) == [1, 3, 4, 6, 7, 8]

    segment_nine = digit_to_segment[3] | digit_to_segment[4]
    digit_to_segment[9] = segment_nine

    assert sorted(digit_to_segment.keys()) == [1, 3, 4, 6, 7, 8, 9]

    left_lower_segment = digit_to_segment[8] - digit_to_segment[9]
    segment_five = digit_to_segment[6] - left_lower_segment
    digit_to_segment[5] = segment_five

    assert sorted(digit_to_segment.keys()) == [1, 3, 4, 5, 6, 7, 8, 9]

    left_side_segment = digit_to_segment[8] - digit_to_segment[3]
    right_side_segment = digit_to_segment[1]
    top_and_bottom_segment = digit_to_segment[9] - digit_to_segment[4]
    segment_zero = left_side_segment | right_side_segment | top_and_bottom_segment
    digit_to_segment[0] = segment_zero

    assert sorted(digit_to_segment.keys()) == [0, 1, 3, 4, 5, 6, 7, 8, 9]

    middle_segment = digit_to_segment[8] - digit_to_segment[0]
    right_top_segment = digit_to_segment[8] - digit_to_segment[6]
    segment_two = top_and_bottom_segment | middle_segment | right_top_segment | left_lower_segment
    digit_to_segment[2] = segment_two

    assert sorted(digit_to_segment.keys()) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    segment_to_digit = {segment: digit for digit, segment in digit_to_segment.items()}

    part_2_output_number = ""
    for segment in output_segments:
        digit = segment_to_digit.get(segment)

        if digit in (1, 4, 7, 8):
            part_1_count += 1

        part_2_output_number += str(digit)

    part_2_sum += int(part_2_output_number)

print(part_1_count, part_2_sum)
