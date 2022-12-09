#! /usr/bin/env python3
import os
from itertools import repeat
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    return [[int(x) for x in line.strip()] for line in input.readlines()]

DIRECTIONS = ['UP','DOWN','LEFT','RIGHT']

def trees_in_direction(forest, tree, direction):
  height, width = len(forest), len(forest[0])
  x, y = tree
  return {
    'UP': ((i,j) for i,j in zip(range(x-1,-1,-1), repeat(y))),
    'DOWN': ((i,j) for i,j in zip(range(x+1,height), repeat(y))),
    'LEFT': ((i,j) for i,j in zip(repeat(x), range(y-1,-1,-1))),
    'RIGHT': ((i,j) for i,j in zip(repeat(x), range(y+1, width))),
  }[direction]

def visible_in_direction(forest, tree, direction):
  x, y = tree
  tree_height = forest[x][y]
  for i,j in trees_in_direction(forest, tree, direction):
    if forest[i][j] >= tree_height:
      return False
  return True

def is_visible(forest, tree):
  return any(visible_in_direction(forest, tree, direction) for direction in DIRECTIONS)

def view_in_direction(forest, tree, direction):
  x, y = tree
  tree_height = forest[x][y]
  view = 0
  for i,j in trees_in_direction(forest, tree, direction):
    view += 1
    if forest[i][j] >= tree_height:
      break
  return view

def scenic_score(forest, tree):
  return reduce(
    lambda x,y: x*y,
    (view_in_direction(forest, tree, direction) for direction in DIRECTIONS)
  )

def process_part_1(forest):
  height, width = len(forest), len(forest[0])
  nb_of_trees_on_edge = height*2 + width*2 - 4
  inner_trees = ((i,j) for i in range(1,height-1) for j in range(1,width-1))
  visible_inner_trees = [tree for tree in inner_trees if is_visible(forest, tree)]
  return nb_of_trees_on_edge + len(visible_inner_trees)

def process_part_2(forest):
  height, width = len(forest), len(forest[0])
  trees = ((i,j) for i in range(height) for j in range(width))
  return max(scenic_score(forest, tree) for tree in trees)

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))

# Tests
assert is_visible([[3,3,3],[3,4,3],[3,3,3]], (1,1)) == True
assert is_visible([[3,3,3],[3,3,3],[3,3,3]], (1,1)) == False
assert is_visible([[3,3,3],[1,2,1],[3,3,3]], (1,1)) == True
assert is_visible([[3,2,3],[3,2,3],[3,1,3]], (1,1)) == True
assert is_visible([[5,5,5,5,5],[4,3,4,0,5],[5,5,5,5,5]], (1,2)) == False
assert is_visible([[5,5,5,5,5],[4,3,3,0,2],[5,5,5,5,5]], (1,2)) == True

TEST_FOREST = parse(TEST_FILE)
assert view_in_direction(TEST_FOREST, (3, 2), 'UP') == 2
assert view_in_direction(TEST_FOREST, (3, 2), 'LEFT') == 2
assert view_in_direction(TEST_FOREST, (3, 2), 'DOWN') == 1
assert view_in_direction(TEST_FOREST, (3, 2), 'RIGHT') == 2

assert view_in_direction(TEST_FOREST, (3, 4), 'UP') == 3

assert scenic_score(TEST_FOREST, (1, 2)) == 4
assert scenic_score(TEST_FOREST, (3, 2)) == 8

assert process_part_1(TEST_FOREST) == 21
assert process_part_2(TEST_FOREST) == 8