#!/usr/bin/python
from pyDes import *

class NameBuilder(object):
    """
    Helper Class for generating obfuscated name
    """
    def __init__(self):
        self.cache = {}

    def check_cache(self, key):
        if key in self.cache.keys():
            return self.cache.get(key)
        else:
            return None

    def _create_tag(self, key):
        raise NotImplementedError("Should implementd this")

    def create_tag(self, key):
        result = self.check_cache(key)
        if result:
            return result
        else:
            result = self._create_tag(key)
            self.cache[key] = result
            return result
