#!/usr/bin/python

from NameBuilder import *

class DictNameBuilder(NameBuilder):
    def __init__(self):
        NameBuilder.__init__(self)
        self.first_letter_dict = map(chr, range(97,123))
        self.first_letter_dict.extend(map(chr, range(65, 91)))
        self.first_letter_dict.extend(["_"])
        self.first_dict_len = len(self.first_letter_dict)

        self.other_letter_dict = map(chr, range(48, 57))
        self.other_letter_dict.extend(self.first_letter_dict)
        self.other_dict_len = len(self.other_letter_dict)
        self.cindex = 0

    def _create_tag(self, key):
        index = self.cindex

        result = self.first_letter_dict[index % self.first_dict_len]
        index /= self.first_dict_len

        while index > 0:
            result += self.other_letter_dict[index % self.other_dict_len]
            index /= self.other_dict_len
        self.cindex += 1
        return result
