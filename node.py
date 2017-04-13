class Node:
  def __init__(self):
    self.label = None
    self.children = {}
    self.name = None

  def get_label(self):
      return self.label

  def get_name(self):
      return self.name

  def get_children(self):
      return self.children

  def add_child(self, node, value):
      self.children[value] = node
      return self

  def print_node(self):
      print "Node label: ", self.label, " name ", self.name
      print "Number of children: ", len(self.children)
      for child in self.children:
          child.print_node()
      return self

#test cases for add_child
#node1 = Node()
#node1.name = "PAtt"
#node2 = Node()
#node2.name = "CAtt"
#node1.add_child(node2,'y')
#print node1.get_children()
#print node1.get_children()['y'].name
