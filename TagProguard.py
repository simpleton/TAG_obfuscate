#!/usr/bin/env python

import os
import fnmatch
import re
import fileinput
import time
import sys
import util
from NameBuilder import NameBuilder
from DictNameBuilder import DictNameBuilder
from EncryptionNameBuilder import EncryptionNameBuilder
from TagParser import TagParser

DEBUG = False

def _print( *params ):
    if DEBUG:
        print params
    return


class TagProguard(object):
    """
    use some obfuscated string to replace TAG string in java source code
    """
    def __init__(self, fd, reg_list):
#        self.name_builder = DictNameBuilder()
        self.name_builder = EncryptionNameBuilder()
        self.mappingfd = fd
        self.reg_list = reg_list

    def write_map_log(self, fd, original, new, line):
        self.mappingfd.write("%s : %s original:%s" % (new, original, line))

    def match(self, line):
        result = None
        for r in self.reg_list:
            result = r.reg.match(line)
            if result:
                return result, r
        return None, None

    def obfuscate(self, filepath):
        for line in fileinput.input(filepath, inplace=1, mode="rb"):
#            if any(r.reg.match(line) for r in self.reg_list):
            result , tagregex  = self.match(line)
            if result is not None:
                original_tag = tagregex.value
                if original_tag is None:
                    original_tag = result.group(1)
                original_tag = self._add_quote(original_tag)
                new_tag = self._add_quote(self.name_builder.create_tag(original_tag))
                print self.replace_tag(line, original_tag, new_tag),
            else:
                if len(line) > 0:
                    print line,
        fileinput.close()

    def replace_tag(self, line, original_tag, new_tag):
        result = line.replace(original_tag, new_tag)
        self.write_map_log(self.mappingfd, original_tag, new_tag, line)
        return result

    def _extract_quote(self, string):
        if string.startswith('"'):
            return string[1:-1]
        else:
            return string

    def _add_quote(self, string):
        if string.startswith('"'):
            return string
        else:
            return "".join(['"', string, '"'])
