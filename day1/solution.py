#! /opt/homebrew/bin/python3
import os

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    chunks = input.read().split('\n\n')
    return ((int(line.strip()) for line in chunk.split('\n')) for chunk in chunks)

def process_part_1(elves_snacks):
  return max(sum(snacks) for snacks in elves_snacks)

def process_part_2(elves_snacks):
  top_three_elves = sorted(sum(snacks) for snacks in elves_snacks)[-3:]
  return sum(top_three_elves)

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))

# Tests
assert process_part_1(parse(TEST_FILE)) == 24000
assert process_part_2(parse(TEST_FILE)) == 45000