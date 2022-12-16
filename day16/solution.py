#! /usr/bin/env python3
import os
import re
from collections import namedtuple
from itertools import count

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

Node = namedtuple("Node", "value to")

LINE_PATTERN = re.compile(
  r'^Valve (?P<from>[A-Z]{2}) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<to>[A-Z, ]*)(\s|$)')
def parse(file):
  def parse_line(line):
    match = LINE_PATTERN.search(line)
    node = Node(int(match.group('rate')), match.group('to').split(', '))
    return (match.group('from'), node)
  with open(file) as input:
    return dict([parse_line(line.strip()) for line in input.readlines()])

def traverse(graph, valves_to_open, start, total_time):
  best_found = 0

  def aux(valves_to_open, current, time_left=30, total_pressure=0, current_pressure=0):
    nonlocal best_found

    pressure_if_we_stay = total_pressure + (time_left * current_pressure)

    if pressure_if_we_stay > best_found:
      best_found = pressure_if_we_stay
      print(best_found)
    
    if time_left == 0:
      return total_pressure

    if len(valves_to_open) == 0:
      return pressure_if_we_stay

    # heuristic
    valves = sorted((graph[valve].value for valve in valves_to_open), reverse=True)
    max_future_pressure = sum(time * valve for time, valve in zip(range(time_left, -1, -2), valves))
    max_potential_pressure = pressure_if_we_stay + max_future_pressure
    if max_potential_pressure < best_found:
      return 0

    node = graph[current]

    possibles = []
    # If current valve is closed, we can open it
    if current in valves_to_open:
      possibles.append(aux(valves_to_open - {current}, current, time_left - 1, total_pressure + current_pressure, current_pressure + node.value))
    # Otherwise, visit other nodes
    for neighbour in node.to:
      possibles.append(aux(valves_to_open, neighbour, time_left - 1, total_pressure + current_pressure, current_pressure))
    return max(possibles)
  return aux(valves_to_open, start, total_time)

def process_part_1(graph):
  valves_to_open = {valve for valve,node in graph.items() if node.value > 0}
  return traverse(graph, valves_to_open, 'AA', 30)

# Solution
print(process_part_1(parse(INPUT_FILE))) # 1880

# Tests
assert process_part_1(parse(TEST_FILE)) == 1651