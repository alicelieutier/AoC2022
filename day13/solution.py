#! /usr/bin/env python3
import os
from functools import cmp_to_key

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_part_1(file):
  def parse_chunk(chunk):
    left, right = chunk.split('\n')
    return eval(left), eval(right)
  with open(file) as input:
    return [parse_chunk(chunk) for chunk in input.read().split('\n\n')]

def parse_part_2(file):
  with open(file) as input:
    return [eval(line) for line in input.read().split('\n') if len(line) > 0]

def compare(left, right):
  if type(left) == int and type(right) == int:
    return left - right
  if type(left) == list and type(right) == list:
    for l, r in zip(left, right):
      if compare(l, r) != 0:
        return compare(l, r)
    return len(left) - len(right)
  if type(left) == int and type(right) == list:
    return compare([left], right)
  if type(left) == list and type(right) == int:
    return compare(left, [right])

def process_part_1(pairs):
  return sum(
    index + 1 if compare(*pair) < 0 else 0
    for index, pair in enumerate(pairs)
  )

def process_part_2(expressions):
  expressions.append([[2]])
  expressions.append([[6]])
  ordered = sorted(expressions, key=cmp_to_key(compare))
  t1 = ordered.index([[2]]) + 1
  t2 = ordered.index([[6]]) + 2
  return t1 * t2

# Solution
print(process_part_1(parse_part_1(INPUT_FILE)))
print(process_part_2(parse_part_2(INPUT_FILE)))

# Tests
assert compare([4], 4) == 0
assert compare([4, 6], [4, 6]) == 0
assert compare([4, [6]], [4, 6]) == 0
assert compare([3], [4]) < 0
assert compare([30], [4]) > 0
assert compare([3, 3], [3]) > 0
assert compare([], [4]) < 0
assert compare([9,7,6], [[8]]) > 0
assert compare([[8]], [9,7,6]) < 0
assert compare([[[]]], [[]]) > 0

assert process_part_1(parse_part_1(TEST_FILE)) == 13
assert process_part_2(parse_part_2(TEST_FILE)) == 140
