#! /opt/homebrew/bin/python3
import os

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

class FileTree:
  def __init__(self, name, parent=None, dir=True, size=0):
    self.name = name
    self.dir = dir
    self._size = size
    self.parent = parent
    self.children = []

  def __repr__(self):
    return f"{'dir' if self.dir else 'file'} {self.name} {self._size}"

  def addChild(self, filetree):
    if self.dir != True:
      raise Exception("Trying to add a child to a non directory")
    self.children.append(filetree)

  def getSize(self):
    if self.dir != True:
      return self._size
    return sum(child.getSize() for child in self.children)

  def getChildByName(self, name):
    return [dir for dir in self.children if dir.name == name][0]
    
def parse(file):
  with open(file) as input:
    return [line.strip() for line in input.readlines()]

def parseTree(lines):
  directories = []
  tree = None
  current_dir = None
  for line in lines:
    if line.startswith('$ cd '):
      dirname = (line.split())[2]
      if tree is None:
        tree = FileTree(dirname, parent=None, dir=True)
        current_dir = tree
        directories.append(tree)
      elif dirname == '..':
        current_dir = current_dir.parent
      else:
        current_dir = current_dir.getChildByName(dirname)
    elif line == '$ ls':
      continue
    else:
      if line.startswith('dir'):
        dirname = (line.split())[1]
        dir = FileTree(dirname, parent=current_dir, dir=True)
        current_dir.addChild(dir)
        directories.append(dir)
      else:
        size_str, name = line.split()
        size = int(size_str)
        file = FileTree(name, parent=current_dir, size=size, dir=False)
        current_dir.addChild(file)
  return tree, directories

def process_part_1(lines):
  _, directories = parseTree(lines)
  return sum(dir.getSize() for dir in directories if dir.getSize() <= 100000)

TOTAL_DISK_SPACE = 70000000
SPACE_NEEDED = 30000000

def process_part_2(lines):
  tree, directories = parseTree(lines)
  space_to_clear = SPACE_NEEDED - (TOTAL_DISK_SPACE - tree.getSize())
  # size of smallest directory of at least size 'space_to_clear'
  return min(dir.getSize() for dir in directories if dir.getSize() >= space_to_clear)

# Solution
print(process_part_1(parse(INPUT_FILE)))
print(process_part_2(parse(INPUT_FILE)))

# Tests
assert process_part_1(parse(TEST_FILE)) == 95437
assert process_part_2(parse(TEST_FILE)) == 24933642