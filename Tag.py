#!/usr/bin/env python

class Tag(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value
