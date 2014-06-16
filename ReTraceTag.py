#!/usr/bin/python
import os
import fnmatch
import fileinput
import re
from Replacement import Replacement
class Retrace(object):
    def __init__(self, mapping_file):
        self.mapping = self.parse_tag_mapping(mapping_file)

    def parse_tag_mapping(self, mapping_file):
        mapping = {}
        with open(mapping_file, "r") as fd:
            for line in fd:
                mlist = line.split()
                value = mapping.get(mlist[0])
                if not value:
                    mapping[mlist[0]] = mlist[2]
                else:
                    if mlist[2] != value:
                        raise Exception("Mapping Error")
        return mapping

    def retrace(self, log_file):
        for line in fileinput.input(log_file, inplace=True):
            mlist = re.split('[\[\]]', line)
            if len(mlist) > 7:
                original_tag = mlist[7]
                print self.replace_tag(line, original_tag, self.mapping.get(original_tag))
        fileinput.close()

    def replace_tag(self, line, original_tag, new_tag):
        if new_tag:
            original_line = line
            repl =  Replacement('[%s]' % new_tag)
            result = re.sub('\[%s\]' % original_tag, repl, line)
        else:
            result = line
        return result


def find_all_files_with_suffix(relative_path, suffix):
    matches = []
    for root, firnames, filenames in os.walk(relative_path):
        for filename in fnmatch.filter(filenames, suffix):
            matches.append(os.path.relpath(os.path.join(root, filename), relative_path))
    return matches

if __name__ == "__main__":
    log_files = find_all_files_with_suffix("./", "*.savelog.txt")
    retrace = Retrace("TagMapping.txt")
    for log_file in log_files:
        retrace.retrace(log_file)


