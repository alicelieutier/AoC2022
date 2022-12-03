#! /opt/homebrew/bin/python3
import os

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    return [line.strip() for line in input.readlines()]

def priority(item):
  ascii = ord(item)
  if ascii > 96:
    return ascii - 96
  return ascii - 38

def item_in_both_compartments(items):
  half = len(items)//2
  return (set(items[:half]) & set(items[half:])).pop()

def common_item_in_backpacks(b1, b2, b3):
  return (set(b1) & set(b2) & set(b3)).pop()

# grouper('ABCDEFG', 3) --> ABC DEF
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)

def process_part_1(lines):
  return sum(priority(item_in_both_compartments(items)) for items in lines)

def process_part_2(lines):
  return sum(priority(common_item_in_backpacks(*backpacks)) for backpacks in grouper(lines, 3))

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))

# Tests
assert priority('a') == 1
assert priority('z') == 26
assert priority('L') == 38
assert priority('Z') == 52

assert item_in_both_compartments('abac') == 'a'
assert item_in_both_compartments('abca') == 'a'

assert common_item_in_backpacks(
  'vJrwpWtwJgWrhcsFMMfFFhFp',
  'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
  'PmmdzqPrVvPwwTWBwg') == 'r'

assert process_part_1(parse(TEST_FILE)) == 157
assert process_part_2(parse(TEST_FILE)) == 70