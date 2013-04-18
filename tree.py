#!/usr/bin/env python

"""
oneline tree with simple search and add function

ref: https://gist.github.com/hrldcpr/2012250

Date: 2013/4/18

"""

from collections import defaultdict
from pprint import pprint

# one-line tree
tree = lambda: defaultdict(tree)

# converts to normal dicts
dicts = lambda t: {k: dicts(t[k]) for k in t}

# pretty print the tree
print_tree = lambda t: pprint(dicts(t))

# determine if node is leaf
is_leaf = lambda n: n == {}

# search node in the tree
# returns the node if found, None otherwise.
def tree_search_node(t, key):
    if is_leaf(t): return None
    for node in t:
        if key == node: return t[node]
        found = tree_search_node(t[node], key)
        if found is not None: return found
    return None

# add a node in the tree under a parent node
# returns True if added successfully, False otherwise.
def tree_add_node(t, parent, node):
    p_node = tree_search_node(t, parent)
    if p_node is None: return False
    # add node
    p_node[node]
    return True

# add a distinct node in the tree under a parent node.
# The node must not be existent in the tree. 
# returns True if the node is distinct and added successfully
def tree_add_node_distinct(t, parent, node):
    found = tree_search_node(t, node)
    if found is None:
        return tree_add_node(t, parent, node)
    return False

# ===============================

# testing function, serves as an example of using it
def test():

    # create the tree manually
    a = tree()
    a['top']['hello']
    a['top']['test']['now']

    # test if a node is leaf
    print is_leaf(a)
    print is_leaf(a['top'])
    print is_leaf(a['top']['hello'])
    print is_leaf(a['top']['test'])
    print is_leaf(a['top']['test']['now'])

    # searching nodes
    r = tree_search_node(a, 'hello')
    print "Result:", dicts(r)
    r = tree_search_node(a, 'now')
    print "Result:", dicts(r)
    r = tree_search_node(a, 'top')
    print "Result:", dicts(r)
    r = tree_search_node(a, 'test')
    print "Result:", dicts(r)
    r = tree_search_node(a, 'not exist')
    if r is None:
        print "No Result"

    # adding nodes
    print "adding nodes..."
    print_tree(a)
    tree_add_node(a, 'hello', 'new')
    print_tree(a)
    tree_add_node(a, 'hello', 'new2')
    print_tree(a)
    tree_add_node(a, 'now', 'and then')
    print_tree(a)
    tree_add_node(a, 'not_exist', 'okok')
    print_tree(a)

    # create another tree by random ints
    import random
    b = tree()
    b[0] # top node
    for i in range(10): # add first level nodes
        tree_add_node_distinct(b, 0, random.randint(1,100))
    for i in range(1000): # randomly adds some nodes
        tree_add_node_distinct(b, random.randint(1,100), random.randint(1,100))
    print_tree(b)

if __name__ == '__main__':
    test()
