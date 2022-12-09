#! /usr/bin/env python3
import os
from itertools import pairwise

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
PART_2_TEST_FILE = f'{os.path.dirname(__file__)}/part2_test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  def parse_line(line):
    direction, steps = line.strip().split()
    return direction, int(steps)

  with open(file) as input:
    return [parse_line(line) for line in input.readlines()]

def atomic_directions(directions):
  for direction, steps in directions:
    for _ in range(steps):
      yield direction

def move_in_direction(position, move):
  return (position[0] + move[0], position[1] + move[1])

def step(previous_tail, new_head):
  x = new_head[0] - previous_tail[0]
  y = new_head[1] - previous_tail[1]
  if abs(x) < 2 and abs(y) < 2: # head still in range
    return previous_tail
  if y == 0: # head in the same column
    return move_in_direction(previous_tail, (x / abs(x), 0))
  if x == 0: # head in the same row
    return move_in_direction(previous_tail, (0, y / abs(y)))
  # otherwise, the tail always moves one step diagonally to keep up
  return move_in_direction(previous_tail, (x / abs(x), y / abs(y)))
  
DIRECTIONS = {
  'U': (1,0),
  'D': (-1,0),
  'R': (0,1),
  'L': (0,-1),
}

def process_part_1(moves):
  tail = (0,0)
  head = (0,0)
  tail_visited = {(0,0)}
  for move in atomic_directions(moves):
    head = move_in_direction(head, DIRECTIONS[move])
    tail = step(tail, head)
    tail_visited.add(tail)
  return len(tail_visited)

def process_part_2(moves):
  rope = [(0,0) for _ in range(10)]
  tail_visited = {(0,0)}

  for move in atomic_directions(moves):
    rope[0] = move_in_direction(rope[0], DIRECTIONS[move])
    for local_head_index, local_tail_index in pairwise(range(10)):
      rope[local_tail_index] = step(rope[local_tail_index], rope[local_head_index])
    tail_visited.add(rope[9])
  return len(tail_visited)

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))

# Tests

# .....    .....    .....
# .TH.. -> .T.H. -> ..TH.
# .....    .....    .....

assert step((1,1), (1,3)) == (1,2)

# ...    ...    ...
# .T.    .T.    ...
# .H. -> ... -> .T.
# ...    .H.    .H.
# ...    ...    ...

assert step((1,1), (3,1)) == (2,1)

# head stays in range, tail doesn't move
assert step((3,3), (2,3)) == (3,3)
assert step((3,3), (3,4)) == (3,3)
assert step((0,2), (1,1)) == (0,2)

# if the head is out of range and not on the same row/column
# the tail always moves one step diagonally to keep up

# .....    .....    .....
# .....    ..H..    ..H..
# ..H.. -> ..... -> ..T..
# .T...    .T...    .....
# .....    .....    .....

assert step((3,1), (1,2)) == (2,2)

# .....    .....    .....
# .....    .....    .....
# ..H.. -> ...H. -> ..TH.
# .T...    .T...    .....
# .....    .....    .....

assert step((3,1), (2,3)) == (2,2)

assert process_part_1(parse(TEST_FILE)) == 13

assert process_part_2(parse(TEST_FILE)) == 1
assert process_part_2(parse(PART_2_TEST_FILE)) == 36