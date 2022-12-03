#! /opt/homebrew/bin/python3
import os

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse(file):
  with open(file) as input:
    return [tuple(line.strip().split()) for line in input.readlines()]

# The score for a single round is the score for the shape you selected
# (1 for Rock, 2 for Paper, and 3 for Scissors)
# plus the score for the outcome of the round
# (0 if you lost, 3 if the round was a draw, and 6 if you won).

 
OUTCOME_SCORE = {
  'A': {'Rock': 3, 'Paper': 6, 'Scissors': 0}, # opponent chooses Rock
  'B': {'Rock': 0, 'Paper': 3, 'Scissors': 6}, # opponent chooses Paper
  'C': {'Rock': 6, 'Paper': 0, 'Scissors': 3} # opponent chooses Scissors
}
SHAPE_SCORE = {'Rock': 1, 'Paper': 2, 'Scissors': 3}

def score(opponent, me):
  outcome = OUTCOME_SCORE[opponent][me]
  shape = SHAPE_SCORE[me]
  return outcome + shape

PART_1_CODE = {'X': 'Rock', 'Y': 'Paper', 'Z': 'Scissors'}

def process_part_1(guide):
  return sum(score(opponent, PART_1_CODE[me]) for opponent, me in guide)

# X means you need to lose,
# Y means you need to end the round in a draw,
# and Z means you need to win.
PART_2_STRATEGY = {
  'A': {'X': 'Scissors', 'Y': 'Rock', 'Z': 'Paper'}, # opponent chooses Rock
  'B': {'X': 'Rock', 'Y': 'Paper', 'Z': 'Scissors'}, # opponent chooses Paper
  'C': {'X': 'Paper', 'Y': 'Scissors', 'Z': 'Rock'} # opponent chooses Scissors
}

def process_part_2(guide):
  return sum(score(opponent, PART_2_STRATEGY[opponent][me]) for opponent, me in guide)

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))

# Tests
assert process_part_1(parse(TEST_FILE)) == 15
assert process_part_2(parse(TEST_FILE)) == 12
