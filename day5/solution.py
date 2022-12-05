#! /opt/homebrew/bin/python3
import os
import re

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  # eg:2-4,6-8
  LINE_PATTERN = re.compile(r'^move (?P<nb_of_crates>\d+) from (?P<start>\d+) to (?P<end>\d+)(\s|$)')
  def parse_move(line):
    match = LINE_PATTERN.search(line)
    # adjust stack indices to be 0-indexed
    return int(match.group('nb_of_crates')), int(match.group('start')) - 1, int(match.group('end')) - 1

  def parse_stacks(lines):
    nb_of_stacks = int((lines[-1].split())[-1])
    stacks = [[] for _ in range(nb_of_stacks)]
    # [Z] [M] [P]
    #  1   5   9 etc.
    stack_line_indices = list(range(1, 4*nb_of_stacks, 4))
    for line in (lines[i] for i in range(len(lines)-2, -1, -1)):
      for index, stack in zip(stack_line_indices, stacks):
        if line[index] != ' ':
          stack.append(line[index])
    return stacks

  with open(file) as input:
    stack_lines, move_lines = input.read().split('\n\n')
    moves = [parse_move(line) for line in move_lines.split('\n')]
    stacks = parse_stacks(stack_lines.split('\n'))
    return stacks, moves

def process_part_1(stacks, moves):
  for nb_of_crates, start, end in moves:
    for _ in range(nb_of_crates):
      stacks[end].append(stacks[start].pop())
  return ''.join(stack[-1] for stack in stacks)


# Solution
print(process_part_1(*parse(INPUT_FILE)))

# Tests
assert process_part_1(*parse(TEST_FILE)) == 'CMZ'