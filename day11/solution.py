#! /usr/bin/env python3
import os, re, operator
from functools import reduce

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

class Monkey:
  def __init__(self, id, starting_items, op, second_term, divider, true_id, false_id):
    self.inspection_counter = 0
    self._id = id
    self.items = starting_items
    self._operation = lambda value: op(value, value if second_term == 'old' else int(second_term))
    self.divider = divider
    self._if_true = true_id
    self._if_false = false_id

  def __repr__(self):
    return f'''<Monkey id {self._id} has inspected {self.inspection_counter} items>'''

  def add_item(self, item):
    self.items.append(item)

  def __inspect(self, worry):
    self.inspection_counter += 1
    return self._operation(worry)

  def turn(self, monkeys, relief_method):
    items_to_inspect = self.items
    self.items = []
    for worry in items_to_inspect:
      worry = self.__inspect(worry)
      worry = relief_method(worry)
      if worry % self.divider == 0:
        monkeys[self._if_true].add_item(worry)
      else:
        monkeys[self._if_false].add_item(worry)

def parse(file):
  with open(file) as input:
    return input.read().split('\n\n')

MONKEY_RE = re.compile(r'''^Monkey (?P<id>\d+):
  Starting items: (?P<starting_items>[\d, ]+)
  Operation: new = old (?P<operator>[+*]) (?P<second_term>(old|\d+))
  Test: divisible by (?P<divider>\d+)
    If true: throw to monkey (?P<true_id>\d+)
    If false: throw to monkey (?P<false_id>\d+)(\s|$)''')

def parse_monkey(chunk):
  match = MONKEY_RE.search(chunk)
  return Monkey(
    id=int(match.group('id')),
    starting_items=[int(item) for item in match.group('starting_items').split(', ')],
    op=operator.mul if match.group('operator') == '*' else operator.add,
    second_term=match.group('second_term'),
    divider=int(match.group('divider')),
    true_id=int(match.group('true_id')),
    false_id=int(match.group('false_id')),
  )

def create_monkey_network(chunks):
  monkeys = [parse_monkey(chunk) for chunk in chunks]
  return monkeys

def round(monkeys, relief_method):
  for monkey in monkeys:
    monkey.turn(monkeys, relief_method)

def monkey_business_level(monkeys):
  monkey1, monkey2 = sorted((monkey.inspection_counter for monkey in monkeys), reverse=True)[:2]
  return monkey1 * monkey2

def process_part_1(chunks):
  monkeys = create_monkey_network(chunks)
  for _ in range(20):
    round(monkeys, lambda worry: worry // 3)
  return monkey_business_level(monkeys)

# We need to lower the worry while conserving
# the properties of the division tests.
# Easiest way is to use the LCM as a modulo.
# We observe all dividers are prime numbers, so the LCM
# is equivalent to multiplying all the dividers together
# We'll use the relief factor like this:
#    worry_level = worry_level % relief_factor

def process_part_2(chunks):
  monkeys = create_monkey_network(chunks)
  relief_factor = reduce(lambda a,b: a*b, [monkey.divider for monkey in monkeys])
  for _ in range(10000):
    round(monkeys, lambda worry: (worry % relief_factor))
  return monkey_business_level(monkeys)

# Solution
print(process_part_1(parse(INPUT_FILE))) # 50172
print(process_part_2(parse(INPUT_FILE))) # 11614682178

# Tests
assert process_part_1(parse(TEST_FILE)) == 10605
assert process_part_2(parse(TEST_FILE)) == 2713310158