#! /usr/bin/env python3
import os

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    return [line.strip() for line in input.readlines()]

def gen_x(instructions):
  x = 1
  for instruction in instructions:
    if instruction == 'noop':
      yield x
    else: # addx
      yield x
      yield x
      term = int(instruction.split()[1])
      x += term

def process_part_1(lines):
  values_of_x = list(gen_x(lines))
  significant_frames = [20,60,100,140,180,220]
  return sum(frame*values_of_x[frame-1] for frame in significant_frames)

def process_part_2(lines):
  sprite_position = gen_x(lines)
  screen = []
  for _ in range(6):
    line = []
    for pixel, sprite_pos in zip(range(40), sprite_position):
      if pixel == sprite_pos or pixel == sprite_pos-1 or pixel == sprite_pos+1:
        line.append('#')
      else:
        line.append('.')
    screen.append(''.join(line))
  return screen

# Solution
print(process_part_1(parse(INPUT_FILE)))
print('\n'.join(process_part_2(parse(INPUT_FILE))))

# Tests
SMALL_TEST = ['noop', 'addx 3','addx -5']
assert list(gen_x(SMALL_TEST)) == [1,1,1,4,4]

assert process_part_1(parse(TEST_FILE)) == 13140

assert process_part_2(parse(TEST_FILE)) == [
  '##..##..##..##..##..##..##..##..##..##..',
  '###...###...###...###...###...###...###.',
  '####....####....####....####....####....',
  '#####.....#####.....#####.....#####.....',
  '######......######......######......####',
  '#######.......#######.......#######.....',
]