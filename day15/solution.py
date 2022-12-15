#! /usr/bin/env python3
import os
import re
from itertools import islice
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  def parse_line(line):
    sx,sy,bx,by = (int(number) for number in re.findall(r'\d+', line))
    return (sx,sy),(bx,by)

  with open(file) as input:
    return [parse_line(line) for line in input.readlines()]

def manhattan(a,b):
  return abs(a[0]-b[0]) + abs(a[1]-b[1])

def does_intersect(disc, target_y):
  centre, radius = disc
  return abs(centre[1] - target_y) <= radius

def intersection_range(disc, target_y):
  """return the min and max x for which
  the y line intersects with the disc"""
  centre, radius = disc
  distance = radius - abs(centre[1] - target_y)
  return centre[0] - distance, centre[0] + distance

def tuning_frequency(pos):
  return pos[0] * 4000000 + pos[1]

def range_length(range):
  return range[1] - range[0] + 1

def process_part_1(data, target_y):
  discs = [(s, manhattan(s,b)) for s,b in data]
  ranges = sorted(intersection_range(disc, target_y)
    for disc in discs if does_intersect(disc, target_y))
  if len(ranges) == 0:
    return 0

  first_range_length = range_length(ranges[0])
  first_range_end = ranges[0][1]
  
  def aux (acc, el):
    length, end = acc
    overlap = 0 if el[0] > end else range_length((el[0], min(el[1], end)))
    length = length + range_length(el) - overlap
    return length, max(el[1],end)

  length, _ = reduce(aux, islice(ranges, 1, None), (first_range_length, first_range_end))
  beacons_on_line = {b for _,b in data if b[1] == target_y}
  return length - len(beacons_on_line)

def process_part_2(data, max_coord):
  pass

# Solution
print(process_part_1(parse(INPUT_FILE), 2000000))
# print(process_part_2(parse(INPUT_FILE), 4000000))

# Tests
assert intersection_range(((8,7), 9),10) == (2,14)
assert manhattan((0,0), (1,1)) == 2
assert manhattan((3,7), (-2,9)) == 7

assert process_part_1(parse(TEST_FILE), 10) == 26
# assert process_part_2(parse(TEST_FILE), 20) == 56000011