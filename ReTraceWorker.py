#!/usr/bin/python
import os
import fileinput
import re
from Replacement import Replacement

class RetraceWorker(object):
    def __init__(self, retrace_file):
        yield

    def get_original_value(self , key):
        #implemented by child class
        raise Exception("UNIMPLEMENTED!!!")

    def retrace(self, log_file):
        for line in fileinput.input(log_file, inplace=1, mode="rb"):
            mlist = re.split('[\[\]]', line)
            if len(mlist) > 7:
                original_tag = mlist[7]
                print self.replace_tag(line, original_tag, self.get_original_value(original_tag)),
            else:
                ## line without tag, just print it
                print line,
        fileinput.close()

    def replace_tag(self, line, original_tag, new_tag):
        if new_tag:
            return line.replace(original_tag, new_tag)
        else:
            return line
