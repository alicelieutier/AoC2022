#! /usr/bin/env python3
import os
from itertools import cycle, count

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    return input.read().strip()


# ####

# .#.
# ###
# .#.

# ..#
# ..#
# ###

# #
# #
# #
# #

# ##
# ##

PIECES = [ # origin at left bottom corner
  [(0,0),(0,1),(0,2),(0,3)], # -
  [(0,1),(1,0),(1,1),(1,2),(2,1)], # +
  [(0,0),(0,1),(0,2),(1,2),(2,2),], # _|
  [(0,0),(1,0),(2,0),(3,0)], # |
  [(0,0),(0,1),(1,0),(1,1)], # .
]

def piece_at(piece, pos):
  return {(pos[0]+square[0],pos[1]+square[1]) for square in piece}

def visualise(tower, piece, pos, tower_height):
  piece = piece_at(piece, pos)
  for y in range(tower_height + 7, -1, -1):
    line = []
    for x in range(7):
      if (y,x) in tower:
        line.append('#')
      elif (y,x) in piece:
        line.append('@')
      else:
        line.append('.')
    print(''.join(line))
  print('-----')

WIDTH = 7

# The tall, vertical chamber is exactly seven units wide.
# Each rock appears so that its left edge is two units away
# from the left wall and its bottom edge is three units
# above the highest rock in the room (or the floor, if there isn't one).

def shifted(pos, direction):
  if direction == '>':
    return pos[0],pos[1]+1
  return pos[0],pos[1]-1

def possible(tower, piece, pos):
  for square in piece_at(piece, pos):
    if (square in tower or square[0] < 0
      or square[1] < 0 or square[1] > 6):
      return False
  return True

def top_most(squares):
  return max(square[0] for square in squares)

def move(directions, pieces):
  tower_height = -1
  tower = set()
  while(True):
    yield tower_height
    # appear a piece
    piece = next(pieces)
    pos = tower_height + 4, 2
    # visualise(tower, piece, pos, tower_height)
    while(True):
      direction = next(directions)
      if possible(tower, piece, shifted(pos,direction)):
        pos = shifted(pos,direction)
      if possible(tower, piece, (pos[0]-1, pos[1])):
        pos = pos[0]-1, pos[1]
      else:
        tower |= set(piece_at(piece, pos))
        tower_height = max(tower_height, top_most(piece_at(piece, pos)))
        break

def process_part_1(input):
  directions = cycle(input)
  pieces = cycle(PIECES)
  g = move(directions, pieces)
  height = 0
  for _ in range(2023):
    height = next(g) + 1
  return height

# def process_part_2(input):
#   directions = cycle(input)
#   pieces = cycle(PIECES)
#   g = move(directions, pieces)
#   height = 0
#   for _ in range(1000000000001):
#     height = next(g) + 1
#   return height

# Solution
print(process_part_1(parse(INPUT_FILE)))
# print(process_part_2(parse(INPUT_FILE)))

# Tests
assert process_part_1(parse(TEST_FILE)) == 3068
# assert process_part_2(parse(TEST_FILE)) == 1514285714288