#!/usr/bin/python

class NameBuilder(object):
    """
    Helper Class for generating obfuscated name
    """
    def __init__(self):
        self.first_letter_dict = map(chr, range(97,123))
        self.first_letter_dict.extend(map(chr, range(65, 91)))
        self.first_letter_dict.extend(["_"])
        self.first_dict_len = len(self.first_letter_dict)

        self.other_letter_dict = map(chr, range(48, 57))
        self.other_letter_dict.extend(self.first_letter_dict)
        self.other_dict_len = len(self.other_letter_dict)
        self.cindex = 0

        self.cache = {}

    def _create_tag(self):
        index = self.cindex

        result = self.first_letter_dict[index % self.first_dict_len]
        index /= self.first_dict_len

        while index > 0:
            result += self.other_letter_dict[index % self.other_dict_len]
            index /= self.other_dict_len
        self.cindex += 1
        return result

    def create_tag(self, key):
        result = self.check_cache(key)
        if result:
            return result
        else:
            result = self._create_tag()
            self.cache[key] = result
            return result

    def check_cache(self, key):
        if key in self.cache.keys():
            return self.cache.get(key)
        else:
            return None

