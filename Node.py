#!/usr/bin/python python

class Node(object):

    def __init__(self, name, father):
        self.name = name
        self.father = father
        self.key = ""
        node = self
        while node != None:
            self.key = ".".join([node.name,self.key])
            node = node.father
