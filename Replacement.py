#!/usr/bin/python

class Replacement(object):
    def __init__(self, replacement):
        self.replacement = replacement
        self.matched = None

    def __call__(self, match):
        self.matched = match.group(0)
        return str(self.replacement)
