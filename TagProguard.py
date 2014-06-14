#!/usr/bin/python

import os
import fnmatch
import re
import fileinput
from Replacement import Replacement
from NameBuilder import NameBuilder

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
    def __init__(self, fd, reg):
        self.name_builder = NameBuilder()
        self.mappingfd = fd
        self.reg = reg

    def write_map_log(self, fd, original, new, line):
        self.mappingfd.write("%s : %s original:%s" % (new, original, line))

    def obfuscate(self, filepath):
        for line in fileinput.input(filepath, inplace=True):
            result = self.reg.match(line)
            if result:
                print self.replace_tag(line, self.name_builder.create_tag()),
            else:
                if len(line) > 0:
                    print line,
        fileinput.close()

    def replace_tag(self, line, new_tag):
        original_line = line
        repl =  Replacement('\"%s\"' % new_tag)
        result = re.sub('\".*\"', repl, line)
        self.write_map_log(tag_fd, repl.matched, new_tag, original_line)
        return result



if __name__ == "__main__":
    files = find_all_files_with_suffix("./", "*.java")
    regex = re.compile(r'.*String TAG\s.*\"')

    with open("TagMapping.txt", 'w') as tag_fd:
        tag_progard = TagProguard(tag_fd, regex)
        for file in files:
            tag_progard.obfuscate(file)
