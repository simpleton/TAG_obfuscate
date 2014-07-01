#!/usr/bin/env python

import os
import fnmatch
import re
import fileinput
import time
import sys
from NameBuilder import NameBuilder
from DictNameBuilder import DictNameBuilder
from EncryptionNameBuilder import EncryptionNameBuilder
from TagParser import TagParser

DEBUG = False

def _print( *params ):
    if DEBUG:
        print params
    return

class TagRegex(object):
    def __init__(self, reg, key, value):
        self.reg = reg
        self.key = key
        self.value = value

def find_all_files_with_suffix(relative_path, suffix):
    matches = []
    for root, firnames, filenames in os.walk(relative_path):
        for filename in fnmatch.filter(filenames, suffix):
            matches.append(os.path.relpath(os.path.join(root, filename), relative_path))
    return matches

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

    def obfuscate(self, filepath):
        for line in fileinput.input(filepath, inplace=1, mode="rb"):
#            if any(r.reg.match(line) for r in self.reg_list):
            ret = self.match(line)
            if ret and len(ret) > 1:
                # this is a little tricky, we assume hardcode tag string never as  same as log format string
                original_tag = ret[1].value
                new_tag = self._add_quote(self.name_builder.create_tag(original_tag))
                print self.replace_tag(line, original_tag, new_tag),
            else:
                if len(line) > 0:
                    print line,
        fileinput.close()

    def replace_tag(self, line, original_tag, new_tag):
        result = line.replace(original_tag, new_tag)
        self.write_map_log(tag_fd, original_tag, new_tag, line)
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

def build_reg(tag_k, tag_v):
    if (tag_k.startswith('"')):
        # hardcode string in log function
        str = r'.*Log.*\(\s*%s' % tag_v
    else:
        # use variable
        str = r'.*String\s+%s\s*=\s*%s' % (tag_k, tag_v)
    _print(tag_k , tag_v)
    return TagRegex(re.compile(str), tag_k, tag_v)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print "Please pass the source code's root folder"
        exit(1)

    folder = sys.argv[1]
    files = find_all_files_with_suffix(folder, "*.java")
    tag_parser = None
    print "Starting Tag Proguard......"
    start_time = time.time()
    with open("TagMapping.txt", 'w') as tag_fd:
        for file in files:
            # ignore hidden files
            if any (i.startswith('.') for i in file.split('/')):
                continue
            file = os.path.join(folder, file)
            tag_parser = TagParser()
            regex = []
            for tag in tag_parser.parse(file):
                regex.append(build_reg(tag.name, tag.value))
            tag_progard = TagProguard(tag_fd, regex)
            tag_progard.obfuscate(file)
    now = time.time()
    cost_time = now - start_time
    print "Finish Tag Proguard. Totally cost %d second" % int(cost_time)
