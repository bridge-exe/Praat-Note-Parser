from pathlib import Path
from pprint import pprint


def read_file(input_path):
    with input_path.open() as fh:
        lines = fh.readlines()
    return lines


def write_file(output_path, lines):
    with output_path.open(mode='w') as fh:
        for line in lines:
            fh.write(f'{line}\n')


def replace_undefined(lines):
    modified_lines = [line.split() for line in lines]
    first_defined_pos = get_starting_pos(modified_lines)

    replace_leading_undefined(modified_lines, first_defined_pos)
    replace_trailing_undefined(modified_lines, first_defined_pos)

    output_lines = ['   '.join(line) for line in modified_lines]
    return output_lines


def get_starting_pos(lines):
    for i, line in enumerate(lines):
        if line[0].startswith('Time_s'):
            continue
        elif not line[0].startswith('--undefined--'):
            return i


def replace_leading_undefined(lines, starting_pos):
    current_pos = starting_pos
    while current_pos > 0:
        if lines[current_pos-1][0] == 'Time_S':
            break
        else:
            old_time = float(lines[current_pos][0])
            new_time = "{:.6f}".format(old_time - 0.01)
            lines[current_pos-1][0] = new_time
            current_pos -= 1
    return lines


def replace_trailing_undefined(lines, starting_pos):
    current_pos = starting_pos
    while current_pos < len(lines) - 1:
        if lines[current_pos+1][0] == '--undefined--':
            old_time = float(lines[current_pos][0])
            new_time = "{:.6f}".format(old_time + 0.01)
            lines[current_pos+1][0] = new_time
        current_pos += 1
    return lines



