#!/usr/bin/python
import os
import fnmatch
import fileinput
import re
from Replacement import Replacement
from ReTraceWorker import RetraceWorker

class DictRetraceWorker(RetraceWorker):
    def __init__(self, retrace_file):
        RetraceWorker.__init__(self, retrace_file)
        self.mapping = self.parse_tag_mapping(retrace_file)

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

    def get_original_value(self, key):
        return self.mapping.get(key)
