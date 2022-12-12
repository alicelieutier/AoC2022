#! /usr/bin/env python3
import os
from collections import deque

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    return [line.strip() for line in input.readlines()]

def inside_bounds(heightmap, pos):
  height, width = len(heightmap) , len(heightmap[0])
  x, y = pos
  return x >= 0 and x < height and y >= 0 and y < width

def neighbours(heightmap, pos):
  x,y = pos
  candidates = [(x-1, y),(x+1, y), (x, y-1), (x, y+1)]
  return [(i,j) for i,j in candidates if inside_bounds(heightmap, (i,j))]

def reachable_up(heightmap, pos):
  x,y = pos
  current_height = ord(heightmap[x][y])
  return [(i,j) for i, j in neighbours(heightmap, pos) if ord(heightmap[i][j]) <= current_height + 1]

def reachable_down(heightmap, pos):
  x,y = pos
  current_height = ord(heightmap[x][y])
  return [(i,j) for i, j in neighbours(heightmap, pos) if ord(heightmap[i][j]) >= current_height - 1]

def start_and_end(lines):
  start, end = None, None
  for i, line in enumerate(lines):
    for j, letter in enumerate(line):
      if letter == 'S':
        start = (i,j)
      if letter == 'E':
        end = (i,j)
  return start, end

def get_heightmap(lines):
  start, end = start_and_end(lines)
  heightmap = [list(line) for line in lines]
  si,sj = start
  heightmap[si][sj] = 'a'
  ei,ej = end
  heightmap[ei][ej] = 'z'
  return heightmap, start, end

def shortest_path(heightmap, start, end):
  pathlength_from_start = {start: 0}
  visited = set()
  to_visit = deque()
  pos = start
  while pos != end:
    for neigh in reachable_up(heightmap, pos):
      if neigh in pathlength_from_start:
        pathlength_from_start[neigh] = min(pathlength_from_start[neigh], pathlength_from_start[pos]+1)
      else:
        pathlength_from_start[neigh] = pathlength_from_start[pos]+1
      to_visit.append(neigh)
    visited.add(pos)
    pos = to_visit.popleft()
    while pos in visited:
      pos = to_visit.popleft()
  return pathlength_from_start[end]

def shortest_path_reverse(heightmap, start, end):
  pathlength_from_end = {end: 0}
  visited = set()
  to_visit = deque()
  pos = end
  while heightmap[pos[0]][pos[1]] != 'a' :
    for neigh in reachable_down(heightmap, pos):
      if neigh in pathlength_from_end:
        pathlength_from_end[neigh] = min(pathlength_from_end[neigh], pathlength_from_end[pos]+1)
      else:
        pathlength_from_end[neigh] = pathlength_from_end[pos]+1
      to_visit.append(neigh)
    visited.add(pos)
    pos = to_visit.popleft()
    while pos in visited:
      pos = to_visit.popleft()
  return pathlength_from_end[pos]

def process_part_1(lines):
  heightmap, start, end = get_heightmap(lines)
  return shortest_path(heightmap, start, end)

def process_part_2(lines):
  heightmap, start, end = get_heightmap(lines)
  return shortest_path_reverse(heightmap, start, end)

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))

# Tests

assert reachable_up(['abc','def','ghi'], (0,0)) == [(0,1)]
assert reachable_up(['abc','def','ghi'], (1,1)) == [(0,1),(1,0),(1,2)]
assert reachable_up(['abc','def','ghi'], (2,2)) == [(1,2),(2,1)]

assert process_part_1(parse(TEST_FILE)) == 31
assert process_part_2(parse(TEST_FILE)) == 29