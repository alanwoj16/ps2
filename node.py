class Node:
  def __init__(self):
    self.label = None
    self.children = {}
    self.name = None
    self.mode = None

  def get_label(self):
      return self.label

  def get_name(self):
      return self.name

  def get_children(self):
      return self.children

  def get_mode(self):
      return self.mode

  def add_child(self, node, value):
      self.children[value] = node
      return self
	  
  def remove_descendant(self, node):
	# First, search our direct children for the node
	for child in self.children:
		if self.children[child]==node:
			self.children.pop(child)
			return True
	# The node is not one of our children. Ask each of them in turn to do it.
	for child in self.children:
		if self.children[child].remove_descendant(node):
			return True
	# The node was not found in our tree
	return False

  def print_node(self):
      print "New Node"
      print "Node label: ", self.label, " name: ", self.name
      print "Number of children: ", len(self.children)
      for key in self.children.keys():
          print "Key: " + str(key)
          print "Name: " + str(self.children[key].name)
          print "Label: " + str(self.children[key].label)
          self.children[key].print_node()








#test cases for add_child
#node1 = Node()
#node1.name = "PAtt"
#node2 = Node()
#node2.name = "CAtt"
#node1.add_child(node2,'y')
#print node1.get_children()
#print node1.get_children()['y'].name