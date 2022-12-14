#! /usr/bin/env python3
import os
from itertools import pairwise, count
from collections import namedtuple
from enum import Enum
from PIL import Image


TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

Terrain = Enum('Terrain', ['SOURCE', 'SAND', 'ROCK', 'AIR'])
Point = namedtuple("Point", "x y")

SOURCE = Point(500,0)

class TerrainMap:
  def __init__(self, source=SOURCE):
    self.source = source
    self.map = {source: Terrain.SOURCE}
    self.ymax = 1
    self.floor_depth = None

  def add_terrain(self, pos, terrain):
    self.map[pos] = terrain
    self.ymax = max(self.ymax, pos.y)
  
  def add_rock_lines(self, input_line):
    def coord(point: str) -> Point:
      """takes a "45,5" string and creates a Point(45,5)"""
      x, y = point.split(',')
      return Point(int(x), int(y))

    points = (coord(point) for point in input_line.split(' -> '))
    for a, b in pairwise(points):
      if a.x > b.x or a.y > b.y:
        a,b = b,a
      for x in range(a.x, b.x + 1):
        for y in range(a.y, b.y + 1):
          self.add_terrain(Point(x,y), Terrain.ROCK)
          self.ymax = max(self.ymax, y)

  def add_floor(self, floor_depth):
    self.floor_depth = floor_depth

  def get(self, pos):
    if self.floor_depth is not None and pos.y >= self.floor_depth:
      return Terrain.ROCK
    return self.map.get(pos, Terrain.AIR)

  def get_symbol(self, pos):
    return {
      Terrain.SOURCE: '+',
      Terrain.SAND: 'o',
      Terrain.ROCK: '#',
      Terrain.AIR: '.',
    }[self.get(pos)]
  
  def get_color(self, pos):
    return {
      Terrain.SOURCE: (233, 0, 86),
      Terrain.SAND: (255, 218, 27),
      Terrain.ROCK: (11, 9, 40),
      Terrain.AIR: (120, 190, 230),
    }[self.get(pos)]

  def __repr__(self):
    ymax = self.ymax if self.floor_depth is None else self.floor_depth
    output = []
    for y in range(-1, ymax+1):
      line = []
      for x in range(500 - ymax, 500 + ymax+1):
        line.append(self.get_symbol(Point(x,y)))
      output.append(f"{y: <3} {''.join(line)}")
    return '\n'.join(output)

  def sand_fall(self, pos):
    if self.get(Point(pos.x, pos.y+1)) == Terrain.AIR:
      return Point(pos.x, pos.y+1)
    if self.get(Point(pos.x-1, pos.y+1)) == Terrain.AIR:
      return Point(pos.x-1, pos.y+1)
    if self.get(Point(pos.x+1, pos.y+1)) == Terrain.AIR:
      return Point(pos.x+1, pos.y+1)
    return pos

  def add_sand_no_floor(self):
    while True:
      pos = self.source
      new_pos = self.sand_fall(pos)
      while new_pos != pos and new_pos.y <= self.ymax:
        pos, new_pos = new_pos, self.sand_fall(new_pos)
      if new_pos.y > self.ymax:
        break
      self.add_terrain(pos, Terrain.SAND)
      yield pos

  def add_sand_with_floor(self):
    while True:
      pos = self.source
      new_pos = self.sand_fall(pos)
      while new_pos != pos:
        pos, new_pos = new_pos, self.sand_fall(new_pos)
      if pos == self.source:
        break
      self.add_terrain(pos, Terrain.SAND)
      yield pos
    yield self.source
  
  def add_sand(self):
    if self.floor_depth is not None:
      return self.add_sand_with_floor()
    return self.add_sand_no_floor()

def parse(file):
  terrain = TerrainMap(SOURCE)
  with open(file) as input:
    for line in input.readlines():
      terrain.add_rock_lines(line.strip())
    return terrain

def process_part_1(terrain_map):
  counter = 0
  for _ in terrain_map.add_sand():
    counter += 1
  # print(terrain_map)
  # create_image(terrain_map, 'part2')
  return counter

def process_part_2(terrain_map):
  counter = 0
  terrain_map.add_floor(terrain_map.ymax + 2)
  for _ in terrain_map.add_sand():
    counter += 1
  # print(terrain_map)
  # create_image(terrain_map, 'part2')
  return counter

IMAGE_COUNTER = count()
def create_image(terrain_map, name):
  height,width = terrain_map.ymax + 3, 2*terrain_map.ymax + 3
  img = Image.new('RGB', [width,height], 255)
  data = img.load()
  for x,i in zip(range(img.size[0]), count(499 - terrain_map.ymax)):
    for y,j in zip(range(img.size[1]), count(-1)):
      data[x,y] = terrain_map.get_color(Point(i,j))
  img.save(f'{name}_{next(IMAGE_COUNTER):05}.png')

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))

# Tests
assert process_part_1(parse(TEST_FILE)) == 24
assert process_part_2(parse(TEST_FILE)) == 93