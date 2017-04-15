
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
    missing_attributes(examples)
    return ID3_Helper(examples, default)

def ID3_Helper(examples, default):
    node = Node()
    node.label = None
    if not examples:
        node.label = default
        return node
    elif check_homogenous_target(examples) != False: #checks to see if target values are the same
        node.label = check_homogenous_target(examples)
        return node
    elif check_homogenous_attributes(examples) == True: #checks to see if attribute values are the same
        node.label = mode(examples,'Class')
        return node
    else:
        best = best_attribute(examples) #find best attribute using InfoGain
        a_mode = mode(examples, best) #finds mode value of best attribute
        node.mode = a_mode
        values = find_values(best, examples) #finds possible values of best attribute
        node.name = best
        for val in values:
            examples_filt = filter_ex(val, best, examples) #filters out examples which are not equal to val
            no_best = remove_best(best, examples_filt) #filters out examples with attribute best
            sub_node = ID3_Helper(no_best,mode(examples, "Class"))
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
                test = examples[0].values()[x]
                for ex in examples:
                        if test == ex.values()[x]:
                                continue
                        else:
                                return False
        return True


def mode(examples, a_name):
    dataList = []
    for ex in examples:
        if ex[a_name] == '?':
            continue
        else:
            dataList.append(ex[a_name])
    data = Counter(dataList)
    mode = data.most_common(1)[0][0]
    return mode

def entropy(examples):
    '''
    Calculates entropy of examples
    '''

    # Calculate the frequency of each value of Class
    freq={}
    for example in examples:
        if freq.has_key(example['Class']):
            freq[example['Class']]+=1.0
        else:
            freq[example['Class']]=1

    # Now calculate entropy
    out=0
    for f in freq.values():
        out+=(-f/len(examples)) * math.log(float(f)/len(examples), 2)

    return out

def infogain(examples, attr):
    '''
    Calculates the information gain resulting from splitting on attr
    '''

    # Calculate the frequency of each value of the attribute
    freq={}
    for example in examples:
        if freq.has_key(example[attr]):
            freq[example[attr]]+=1
        else:
            freq[example[attr]]=1

    # Calculate weighted sum of entropy for each subset of examples
    subsetEntropy=0
    for value in freq.keys():
        probability=freq[value]/sum(freq.values())

        # Build a subset of data with this value
        subset=[]
        for example in examples:
            if example[attr]==value:
                subset.append(example)
        subsetEntropy+=probability*entropy(subset)

    # Now subtract the total entropy of this attribute from the entropy of the dataset
    return entropy(examples)- subsetEntropy

def best_attribute(examples):
    attributes=examples[0].keys()
    bestGain=0
    bestAttr=None
    for attribute in attributes:
        gain=infogain(examples, attribute)
        if gain>bestGain:
            bestGain=gain
            bestAttr=attribute
    return bestAttr

def find_values(best, examples):
        values = []
        for ex in examples:
                if ex[best] not in values:
                        values.append(ex[best])
        return values


def filter_ex(val, best, examples):
    examples_copy = deepcopy(examples)
    examples_copy = [ex for ex in examples_copy if ex[best] == val]
    return examples_copy


def remove_best(best, examples):
    examples_copy = deepcopy(examples)
    for ex in examples_copy:
        del ex[best]
    return examples_copy


def missing_attributes(examples):
    class_values = find_values('Class', examples)
    a_names = get_attribute_names(examples)
    for val in class_values:
        for a in a_names:
            exam_copy = deepcopy(examples)
            exam_copy = [ex for ex in exam_copy if ex['Class'] == val]
            a_mode = mode(exam_copy, a)
            for ex in examples:
                if ex[a] == '?':
                    ex[a] = a_mode


def get_attribute_names(examples):
    list = examples[0].keys()
    if 'Class' in list:
        return list[0:-1]
    return list



#test cases for ID3
#data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
#assert ID3(data, 0).label == 1
#data = []
#assert ID3(data,0).label == 0
#data = [dict(b=1, Class='b'), dict(b=1, Class='a'), dict(b=1, Class='b'), dict(b=1, Class='a'), dict(b=1, Class='a')]
#assert ID3(data, 0).label == 'a'
#data = [dict(a=1, b=0, Class=0), dict(a=1, b=1, Class=1)]
#assert ID3(data, 0) == "hi"


#test cases for check_homogenous_target
#data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
#assert check_homogenous_target(data) == 1
#data = [dict(a=1, b= 0, Class = 0)]
#assert check_homogenous_target(data) == 0
#data = [dict(a=1, b=0, Class=0), dict(a=1, b=1, Class=1)]
#assert check_homogenous_target(data) == False

#test cases for check__homogenous_attributes
#data = [dict(a=1, Class=0), dict(a=1, Class=1), dict(a=1, Class=1)]
#assert check_homogenous_attributes(data) == True
#data = [dict(a=1, Class=1), dict(a=1, Class=1), dict(a=0, Class=1)]
#assert check_homogenous_attributes(data) == False
#data = [dict(a=0, Class=0), dict(a=0, Class=1)]
#assert check_homogenous_attributes(data) == True
#data = [dict(a=1,b=1, Class=1), dict(a=1,b=1, Class=1), dict(a=1,b=0, Class=1)]
#assert check_homogenous_attributes(data) == False
#data = [dict(a=1,b=1, Class=1), dict(a=1,b=1, Class=0), dict(a=1,b=1, Class=1)]
#assert check_homogenous_attributes(data) == True


#test cases for mode
#data = [dict(a=1, b=0, Class='a'), dict(a=1, b=2, Class='c'), dict(a=1, b=0, Class='a')]
#assert mode(data,'Class') == 'a'
#data = [dict(a=1, Class='b'), dict(a=1, Class='b'), dict(a=1, Class='d')]
#assert mode(data,'Class') == 'b'
#data = [dict(a=0, Class='q'), dict(a=0, Class='q')]
#assert mode(data,'Class') == 'q'

#test cases for find value
#data = [dict(a=1, b=0, Class='a'), dict(a=1, b=2, Class='c'), dict(a=1, b=0, Class='a')]
#assert find_values('a',data) == [1]
#assert find_values('b',data) == [0,2]


#test cases for filter_ex
#data1 = [dict(a=1, b=0, Class='a'), dict(a=1, b=2, Class='c'), dict(a=1, b=0, Class='a')]
#data2 = [dict(b=0, Class='a'), dict(b=2, Class='c'), dict(b=0, Class='a')]
#assert filter_ex('a', data) == data2

def pruneOneNode(node, examples):
    '''
    Takes in a trained tree and a validation set of examples.  Prune one node in order
    to improve accuracy on the validation data; Which node is found by BFS
    '''
    #get the Validation Accuracy
    BaseValidAcc = test(node,examples)
    BestAcc=BaseValidAcc
    BestTree=node
    nodes=[node]
    while (len(nodes)!=0):
        n=nodes.pop(0)
        for child in n.children:
            nodes.append(n.children[child])
            testTree=deepcopy(node)
            testTree.remove_descendant(n)
            testAcc=test(testTree, examples)
            if testAcc>BestAcc:
                BestAcc=testAcc
                BestTree=testTree
    node=BestTree
    return node

def prune(node, examples):
    '''
    Takes in a trained tree and a validation set of examples.  Prunes nodes in order
    to improve accuracy on the validation data; the precise pruning strategy is up to you.
    '''
    epsilon=0.01 # Will stop attempting to improve when the difference in successive runs falls to or below this value
    # AKA, higher epsilon sacrifices possible performance gains for decreased runtime
    # Note that very low epsilons may overfit the data on which they prune

    while True:
        lastAccuracy=test(node, examples)
        if test(pruneOneNode(node, examples), examples)-lastAccuracy<=epsilon:
            break

def test(node, examples):
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
    of examples the tree classifies correctly).
    '''
    CorrectValue = 0
    totalValue = 0
    for ex in examples:
            totalValue += 1
            temp =  evaluate(node,ex)
            if temp == ex['Class']:
                CorrectValue +=1
    return CorrectValue/totalValue

#test cases for missing attributes
#data1 = [dict(a=1, b='?', Class='a'), dict(a=1, b=2, Class='c'), dict(a=1, b=0, Class='a'), dict(a=1, b=0, Class='a'),
        #dict(a=1, b=2, Class='a'), dict(a=1,b=2, Class='c')]

#test cases for get_attribute_names:
#data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
#assert get_attribute_names(data) == ['a','b']
#data = [dict(a=1, b=0), dict(a=1, b=1)]
#assert get_attribute_names(data) == ['a','b']


#test cases for missing attributes
#data = [dict(a=1, b='?', Class=1), dict(a=1, b=1, Class=1), dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
#missing_attributes(data)
#assert data == [dict(a=1, b=1, Class=1), dict(a=1, b=1, Class=1), dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
#data = [dict(a=1, b=1, Class=1), dict(a='?', b=1, Class=1), dict(a='?', b=0, Class=1), dict(a='?', b=1, Class=1)]
#missing_attributes(data)
#assert data == [dict(a=1, b=1, Class=1), dict(a=1, b=1, Class=1), dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]

def test(node, examples):
    '''
    Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
    of examples the tree classifies correctly).
    '''
    CorrectValue = 0
    totalValue = 0
    for ex in examples:
        totalValue += 1
        temp = evaluate(node,ex)
        if temp == ex['Class']:
            CorrectValue +=1
    return float(CorrectValue)/float(totalValue)

def evaluate(node, example):
    '''
    Takes in a tree and one example.  Returns the Class value that the tree
    assigns to the example.
    '''
    if len(node.get_children())==0: # If the node has no children, we've reached the bottom of our tree
        return node.get_label()

    # If the node has children, then find the one which matches our example data and evaluate using that node
    children=node.get_children()
    for child in children:
        if example[node.get_name()]==child: # If our example value matches the one of this child...
            return evaluate(children[child], example) # Recurse with that child

    a_mode = node.get_mode()
    return evaluate(node.get_children()[a_mode], example)
