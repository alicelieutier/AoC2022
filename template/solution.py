#! /usr/bin/env python3
import os

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    return [line.strip() for line in input.readlines()]

def process_part_1(lines):
  print(list(lines)[:2])
  return 0

# Solution
# print(process_part_1(parse(INPUT_FILE)))

# Tests
assert process_part_1(parse(TEST_FILE)) == 0