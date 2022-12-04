#! /opt/homebrew/bin/python3
import os
import re

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  # eg:2-4,6-8
  LINE_PATTERN = re.compile(r'^(?P<e1min>\d+)-(?P<e1max>\d+),(?P<e2min>\d+)-(?P<e2max>\d+)(\s|$)')
  def parse_line(line):
    match = LINE_PATTERN.search(line)
    e1 = int(match.group('e1min')), int(match.group('e1max'))
    e2 = int(match.group('e2min')), int(match.group('e2max'))
    return (e1, e2)

  with open(file) as input:
    return [parse_line(line) for line in input.readlines()]

def complete_overlap(e1, e2):
  return (e1[0] <= e2[0] and e1[1] >= e2[1]) or (e2[0] <= e1[0] and e2[1] >= e1[1])

def partial_overlap(e1, e2):
  return (e1[0] <= e2[0] and e1[1] >= e2[0]) or (e2[0] <= e1[0] and e2[1] >= e1[0])

def process_part_1(pairs):
  return len([(e1, e2) for e1, e2 in pairs if complete_overlap(e1, e2)])

def process_part_2(pairs):
  return len([(e1, e2) for e1, e2 in pairs if partial_overlap(e1, e2)])

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))


# Tests
assert complete_overlap((2,8),(3,7)) == True
assert complete_overlap((2,8),(1,7)) == False
assert complete_overlap((1,5),(6,7)) == False
assert complete_overlap((3,4),(1,7)) == True
assert complete_overlap((5,8),(5,8)) == True

assert partial_overlap((2,7),(7,8)) == True
assert partial_overlap((2,5),(1,4)) == True
assert partial_overlap((1,5),(6,7)) == False

assert process_part_1(parse(TEST_FILE)) == 2
assert process_part_2(parse(TEST_FILE)) == 4