#!/usr/bin/env python

import sys
import re
import util
import time, os
from SimpleRegTagProguard import SimpleRegTagProguard
from TagProguard import TagProguard
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


def work(func, *argv):
    if not len(*argv) > 1:
        print len(argv)
        print "Please pass the source code's root folder"
        exit(1)

    folder = sys.argv[1]
    print "Starting Tag Proguard......"
    start_time = time.time()

    func(folder)

    now = time.time()
    cost_time = now - start_time
    print "Finish Tag Proguard. Totally cost %d second" % int(cost_time)

def simple_reg_tagproguard_run(folder):
    files = util.find_all_files_with_suffix(folder, "*.java")
    regex = re.compile(r'.*String\s+TAG\d*\s*=\s*\"(.*)\"')
    with open("TagMapping.txt", "w") as tag_fd:
        tag_progard = SimpleRegTagProguard(tag_fd, regex)
        for file in files:
            tag_progard.obfuscate(file)

def ast_tagproguard_run(folder):
    tag_parser = None
    files = util.find_all_files_with_suffix(folder, "*.java")
    with open("TagMapping.txt", 'w') as tag_fd:
        for file in files:
            # ignore hidden files
            if any (i.startswith('.') for i in file.split('/')):
                continue
            _print(file)
            file = os.path.join(folder, file)
            tag_parser = TagParser()
            regex = []
            for tag in tag_parser.parse(file):
                regex.append(build_reg(tag.name, tag.value))
            tag_progard = TagProguard(tag_fd, regex)
            tag_progard.obfuscate(file)

def build_reg(tag_k, tag_v):
    if (tag_k.startswith('"')):
        # hardcode string in log function
        str = r'.*Log.*\(\s*(%s)' % tag_k
    else:
        # use variable
        #str = r'.*String\s+%s\s*=\s*%s' % (tag_k, tag_v)
        if tag_v is None:
            str = r'.*String\s+{}\s*=\s*\"(.*)\"'.format(tag_k)
        else:
            str = r'.*String\s+{}\s*=\s*{}'.format(tag_k, tag_v)
    _print(tag_k , tag_v)
    return TagRegex(re.compile(str), tag_k, tag_v)


if __name__ == "__main__":
    work(simple_reg_tagproguard_run, sys.argv)
#    work(ast_tagproguard_run, sys.argv)
