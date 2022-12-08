#! /opt/homebrew/bin/python3
import os
from itertools import repeat

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    return [list(map(int, line.strip())) for line in input.readlines()]

DIRECTIONS = ['UP','DOWN','LEFT','RIGHT']

def trees_in_direction(forest, tree, direction):
  height, width = len(forest), len(forest[0])
  x, y = tree
  if direction == 'UP':
    return ((i,j) for i,j in zip(range(x-1,-1,-1), repeat(y)))
  if direction == 'DOWN':
    return ((i,j) for i,j in zip(range(x+1,height), repeat(y)))
  if direction == 'LEFT':
    return ((i,j) for i,j in zip(repeat(x),range(y-1,-1,-1)))
  if direction == 'RIGHT':
    return ((i,j) for i,j in zip(repeat(x),range(y+1, width)))

def hidden_in_direction(forest, tree, direction):
  x, y = tree
  tree_height = forest[x][y]
  for i,j in trees_in_direction(forest, tree, direction):
    if forest[i][j] >= tree_height:
      return True

def is_hidden(forest, tree):
  return all(hidden_in_direction(forest, tree, direction) for direction in DIRECTIONS)

def process_part_1(forest):
  height, width = len(forest), len(forest[0])
  inner_trees = ((i,j) for i in range(1,height-1) for j in range(1,width-1))
  hidden_trees = [tree for tree in inner_trees if is_hidden(forest, tree)]
  return height*width - len(hidden_trees)

# Solution
print(process_part_1(parse(INPUT_FILE)))

# Tests
assert is_hidden([[3,3,3],[3,4,3],[3,3,3]], (1,1)) == False
assert is_hidden([[3,3,3],[3,3,3],[3,3,3]], (1,1)) == True
assert is_hidden([[3,3,3],[1,2,1],[3,3,3]], (1,1)) == False
assert is_hidden([[3,2,3],[3,2,3],[3,1,3]], (1,1)) == False
assert is_hidden([[5,5,5,5,5],[4,3,4,0,5],[5,5,5,5,5]], (1,2)) == True
assert is_hidden([[5,5,5,5,5],[4,3,3,0,2],[5,5,5,5,5]], (1,2)) == False

assert process_part_1(parse(TEST_FILE)) == 21