#! /usr/bin/env python3
import os
import re

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

class Monkey:
  def __init__(self, id, starting_items, operation, divider):
    self.inspection_counter = 0
    self._id = id
    self.items = starting_items
    self._divider = divider
    self._if_true = self
    self._if_false = self
    self._operation = self.parse_operation(operation.split())
    

  def __repr__(self):
    return f'''<Monkey id {self._id} has inspected {self.inspection_counter} items>'''

  def parse_operation(self, operation):
    _, _, first_term, operator, second_term = operation
    if first_term != 'old':
      raise Exception('not implemented - first term should be "old" but received {first_term}')
    if operator not in {'*', '+'}:
      raise Exception('not implemented - operator should be * or + but received {operator}')
    def aux(value):
      t1 = value
      t2 = value if second_term == 'old' else int(second_term)
      return t1 * t2 if operator == '*' else t1 + t2
    return aux

  def add_item(self, item):
    self.items.append(item)

  def inspect(self, item):
    self.inspection_counter += 1
    item = self._operation(item)
    item = item // 3
    return item

  def add_if_true_monkey(self, if_true_monkey):
    self._if_true = if_true_monkey

  def add_if_false_monkey(self, if_false_monkey):
    self._if_false = if_false_monkey

  def take_turn(self):
    items_to_inspect = self.items
    self.items = []
    for item_worry_value in items_to_inspect:
      new_item_worry_value = self.inspect(item_worry_value)
      if new_item_worry_value % self._divider == 0:
        self._if_true.add_item(new_item_worry_value)
      else:
        self._if_false.add_item(new_item_worry_value)

def parse(file):
  with open(file) as input:
    return input.read().split('\n\n')

MONKEY_RE = re.compile(r'''^Monkey (?P<id>\d+):
  Starting items: (?P<starting_items>[\d, ]+)
  Operation: (?P<operation>.*)
  Test: divisible by (?P<divider>\d+)
    If true: throw to monkey (?P<true_id>\d+)
    If false: throw to monkey (?P<false_id>\d+)(\s|$)''')

def parse_monkey(chunk):
  match = MONKEY_RE.search(chunk)
  id = int(match.group('id'))
  starting_items = [int(item) for item in match.group('starting_items').split(', ')]
  operation = match.group('operation')
  divider = int(match.group('divider'))
  true_id = int(match.group('true_id'))
  false_id = int(match.group('false_id'))
  monkey = Monkey(id, starting_items, operation, divider)
  return id, monkey, true_id, false_id

def create_monkey_network(chunks):
  monkey_array = [parse_monkey(chunk) for chunk in chunks]
  monkeys = {id: monkey for (id, monkey, _ , _) in monkey_array }
  for id, _, true_id, false_id in monkey_array:
    monkeys[id].add_if_true_monkey(monkeys[true_id])
    monkeys[id].add_if_false_monkey(monkeys[false_id])
  return monkeys

def round(monkeys):
  for i in range(len(monkeys)):
    monkeys[i].take_turn()

def process_part_1(chunks):
  monkeys = create_monkey_network(chunks)
  for _ in range(20):
    round(monkeys)
  monkey1, monkey2 = sorted((monkey.inspection_counter for monkey in monkeys.values()), reverse=True)[:2]
  return monkey1 * monkey2

# Solution
print(process_part_1(parse(INPUT_FILE)))

# Tests
assert process_part_1(parse(TEST_FILE)) == 10605