#! /usr/bin/env python3
import os
import re
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

def intersection(disc, target_y):
  """returns all points with integer coordinates in
  the intersection of a manhattan disc and a 'y' line"""
  # find the point p on the line closest to the centre of the disc
  centre, radius = disc
  p = (centre[0], target_y)
  intersection = set()
  # if p is in the disc, add it, then expand on both sides.
  current = p
  while manhattan(centre, current) <= radius:
    intersection.add(current)
    intersection.add((p[0] - (current[0] - p[0]), target_y))
    current = (current[0]+1, target_y)
  return intersection

def process_part_1(data, target_y):
  discs = [(s, manhattan(s,b)) for s,b in data]
  intersections = reduce(
    lambda a,b: a | b,
    [intersection(disc, target_y) for disc in discs],
  )
  # remove actual beacon positions
  non_beacons_on_line = intersections - set(b for _,b in data)
  return len(non_beacons_on_line)

# Solution
print(process_part_1(parse(INPUT_FILE), 2000000))

# Tests
assert len(intersection(((8,7), 9),10)) == 13
assert manhattan((0,0), (1,1)) == 2
assert manhattan((3,7), (-2,9)) == 7

assert process_part_1(parse(TEST_FILE), 10) == 26