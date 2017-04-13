from node import Node
import math
from collections import Counter
from copy import deepcopy

'''
  Takes in an array of examples, and returns a tree (an instance of Node)
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''


def ID3(examples, default):
    node = Node()
    node.label = None
    if not examples:
        node.label = default
        return node
    elif check_homogenous_target(examples) != False:
        node.label = check_homogenous_target(examples)
        return node
    elif check_homogenous_attributes(examples) == True:
        node.label = mode(examples)
        return node
    else:
        return "hi"
        best = best_attribute(examples)
        values = find_values(best, examples)
        node.name = best
        for val in values:
            examples_sub = filter_ex(best, examples)
            sub_node = ID3(examples_sub,mode(examples))
            node.add_child(sub_node, val)
        return node



def check_homogenous_target(examples):
    value = examples[0]['Class']
    for ex in examples:
        if ex['Class'] == value:
            continue
        else:
            return False
    return value


def check_homogenous_attributes(examples):
    for x in range(0,len(examples[0])-1):
        test = examples[x].values()[x]
        for ex in examples:
            if test == ex.values()[x]:
                continue
            else:
                return False
    return True


def mode(examples):
    dataList = []
    for ex in examples:
        dataList.append(ex['Class'])
    data = Counter(dataList)
    mode = data.most_common(1)[0][0]
    return mode


def best_attribute(examples):
    return "ba"


def find_values(best, examples):
    values = []
    for ex in examples:
        if ex[best] not in values:
            values.append(ex[best])
    return values


def filter_ex(best, examples):
    examples_copy = deepcopy(examples)
    for ex in examples_copy:
        del ex[best]
    return examples_copy


#test cases for ID3
data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
assert ID3(data, 0).label == 1
data = []
assert ID3(data,0).label == 0
data = [dict(b=1, Class='b'), dict(b=1, Class='a'), dict(b=1, Class='b'), dict(b=1, Class='a'), dict(b=1, Class='a')]
assert ID3(data, 0).label == 'a'
data = [dict(a=1, b=0, Class=0), dict(a=1, b=1, Class=1)]
assert ID3(data, 0) == "hi"


#test cases for check_homogenous_target
data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
assert check_homogenous_target(data) == 1
data = [dict(a=1, b= 0, Class = 0)]
assert check_homogenous_target(data) == 0
data = [dict(a=1, b=0, Class=0), dict(a=1, b=1, Class=1)]
assert check_homogenous_target(data) == False

#test cases for check__homogenous_attributes
data = [dict(a=1, Class=0), dict(a=1, Class=1), dict(a=1, Class=1)]
assert check_homogenous_attributes(data) == True
data = [dict(a=1, Class=1), dict(a=1, Class=1), dict(a=0, Class=1)]
assert check_homogenous_attributes(data) == False
data = [dict(a=0, Class=0), dict(a=0, Class=1)]
assert check_homogenous_attributes(data) == True
data = [dict(a=1,b=1, Class=1), dict(a=1,b=1, Class=1), dict(a=1,b=0, Class=1)]
assert check_homogenous_attributes(data) == False
data = [dict(a=1,b=1, Class=1), dict(a=1,b=1, Class=0), dict(a=1,b=1, Class=1)]
assert check_homogenous_attributes(data) == True


#test cases for mode
data = [dict(a=1, b=0, Class='a'), dict(a=1, b=2, Class='c'), dict(a=1, b=0, Class='a')]
assert mode(data) == 'a'
data = [dict(a=1, Class='b'), dict(a=1, Class='b'), dict(a=1, Class='d')]
assert mode(data) == 'b'
data = [dict(a=0, Class='q'), dict(a=0, Class='q')]
assert mode(data) == 'q'

#test cases for find value
data = [dict(a=1, b=0, Class='a'), dict(a=1, b=2, Class='c'), dict(a=1, b=0, Class='a')]
assert find_values('a',data) == [1]
assert find_values('b',data) == [0,2]


#test cases for filter_ex
data1 = [dict(a=1, b=0, Class='a'), dict(a=1, b=2, Class='c'), dict(a=1, b=0, Class='a')]
data2 = [dict(b=0, Class='a'), dict(b=2, Class='c'), dict(b=0, Class='a')]
assert filter_ex('a', data) == data2


def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if node.get_children() == {}: # If the node has no children, we've reached the bottom of our tree
      return node.get_label()
  # If the node has children, then find the one which matches our example data and evaluate using that node
  for child in node.get_children():
      if example[node.get_name()]==child.label: # If our example value matches the one of this child...
          return evaluate(child, example) # Recurse with that child
  # If control flow gets here, we have a problem. No child matched example.
  # TODO: Do we need to handle this case? If so, it should go here. What should be done:
  # Go over the tree, and generate an associative array pairing possible classifications to number of appearances
  # in our tree, and then return the one with greatest number of appearances.
