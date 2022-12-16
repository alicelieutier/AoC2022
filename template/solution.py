#! /usr/bin/env python3
import os
import re

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

LINE_PATTERN = re.compile(r'^move (?P<nb_of_crates>\d+) from (?P<start>\d+) to (?P<end>\d+)(\s|$)')
def parse(file):
  def parse_line(line):
    match = LINE_PATTERN.search(line)
    return int(match.group('nb_of_crates'))
    
  with open(file) as input:
    return [line.strip() for line in input.readlines()]

def process_part_1(lines):
  print(list(lines)[:2])
  return 0

# Solution
# print(process_part_1(parse(INPUT_FILE)))

# Tests
assert process_part_1(parse(TEST_FILE)) == 0