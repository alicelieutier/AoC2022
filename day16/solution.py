#! /usr/bin/env python3
import math
import os
import re
from collections import defaultdict, deque, namedtuple
from itertools import count, permutations

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

def shortest_path(graph, start, end):
  pathlengths = defaultdict(lambda: math.inf)
  visited = set()
  to_visit = deque()
  current = start
  pathlengths[start] = 0
  while current != end:
    if current not in visited:
      for neighbour in graph[current].to:
        pathlengths[neighbour] = min(pathlengths[neighbour], pathlengths[current]+1)
        to_visit.append(neighbour)
      visited.add(current)
    current = to_visit.popleft()
  return pathlengths[current]

def traverse(graph, edges, valves_to_open, start, total_time):
  best_found = 0

  def aux(valves_to_open, current, time_left=30, total_pressure=0, current_pressure=0):
    nonlocal best_found, edges

    if time_left <= 0:
      return total_pressure + time_left*current_pressure

    pressure_if_we_stay = total_pressure + (time_left * current_pressure)

    if pressure_if_we_stay > best_found:
      best_found = pressure_if_we_stay

    if len(valves_to_open) == 0:
      return pressure_if_we_stay

    # heuristic
    valves = sorted((graph[valve].value for valve in valves_to_open), reverse=True)
    max_future_pressure = sum(time * valve for time, valve in zip(range(time_left, -1, -2), valves))
    max_potential_pressure = pressure_if_we_stay + max_future_pressure
    if max_potential_pressure < best_found:
      return 0

    possibles = []
    # If current valve is closed, we can open it
    if current in valves_to_open:
      possibles.append(aux(valves_to_open - {current}, current, time_left - 1, total_pressure + current_pressure, current_pressure + graph[current].value))
    # Otherwise, visit other valves
    for valve in valves_to_open - {current}:
      time_to_reach_valve = edges[current, valve]
      possibles.append(aux(
        valves_to_open,
        valve,
        time_left - time_to_reach_valve,
        total_pressure + time_to_reach_valve*current_pressure,
        current_pressure))
    return max(possibles)
  return aux(valves_to_open, start, total_time)

def process_part_1(graph):
  valves_to_open = {valve for valve,node in graph.items() if node.value > 0}
  # preprocess shortest paths between each pair of "important" valve
  edges = {pair: shortest_path(graph, *pair) for pair in permutations(valves_to_open | {'AA'}, 2)}
  return traverse(graph, edges, valves_to_open, 'AA', 30)

# Solution
print(process_part_1(parse(INPUT_FILE))) # 1880

# Tests
assert process_part_1(parse(TEST_FILE)) == 1651