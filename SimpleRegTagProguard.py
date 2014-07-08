#!/usr/bin/python
import util
import re
import fileinput
from Replacement import Replacement
from EncryptionNameBuilder import EncryptionNameBuilder

class SimpleRegTagProguard(object):
    """
    use some obfuscated string to replace TAG string in java source code
    """
    def __init__(self, fd, reg):
#        self.name_builder = DictNameBuilder()
        self.name_builder = EncryptionNameBuilder()
        self.mappingfd = fd
        self.reg = reg

    def write_map_log(self, fd, original, new, line):
        self.mappingfd.write("%s : %s original:%s" % (new, original, line))

    def obfuscate(self, filepath):
        for line in fileinput.input(filepath, inplace=True):
            result = self.reg.match(line)
            if result:
                original_tag = result.group(1)
                if not self.is_keeped(line):
                    print self.replace_tag(line, original_tag, self.name_builder.create_tag(original_tag)),
                else:
                    print line,
            else:
                if len(line) > 0:
                    print line,
        fileinput.close()

    def _replace_tag(self, line, new_tag):
        original_line = line
        repl =  Replacement('\"%s\"' % new_tag)
        result = re.sub('\".*\"', repl, line)
        self.write_map_log(self.mappingfd, repl.matched, new_tag, original_line)
        return result

    def replace_tag(self, line, original_tag, new_tag):
        result = line.replace(original_tag, new_tag)
        self.write_map_log(self.mappingfd, original_tag, new_tag, line)
        return result

    def is_keeped(self, line):
        if "MicroMessenger_Android_Release" in line:
            return True
        return False
