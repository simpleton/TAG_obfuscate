#!/usr/bin/env python
from model import *
import parser
import sys
from Tag import Tag
from Node import Node



DEBUG = False

def _print( *params ):
    if DEBUG:
        print params

class TagVisitor(Visitor):

    def __init__(self, verbose=False):
        super(TagVisitor, self).__init__(verbose)
        self.tags = []
        self.log_method_list = ['i', 'd', 'e', 'v', 'f', 'w', 'printDebugStack', 'printInfoStack', 'printErrStackTrace']

    #FIXME:should pass the fahter node for helping find the TAG's value
    def visit_MethodInvocation(self, invoke_decl):
        if type(invoke_decl.target) is Name and invoke_decl.target.value == "Log" and invoke_decl.name in self.log_method_list:
            tag_k ,format_str = self.extract_arguments(invoke_decl)
            _print(tag_k, format_str)
            #FIXME: didn't support reference other class's tag
            if '.' in tag_k:
                return True
            tag_v = self.get_tag_value(key = tag_k, domain = None)
            tag = Tag(tag_k, tag_v)
            if tag not in self.tags:
                self.tags.append(tag)
        return True


    def get_tag_value(self, key, domain):
        return None

    def _extract_tag_value(self, elem):
        if hasattr(elem , 'arguments'):
            _print(elem.arguments)
            tag = elem.arguments[0]
        else:
            tag = elem
        if type(tag) is Name:
            tag_v = tag.value
        elif type(tag) is Literal:
            tag_v = tag.value
        elif type(tag) is Additive:
            # FIXME: only extract most left value of the expression
            tag_v = self._extract_tag_value(tag.lhs)
        else:
            raise Exception("tag type error: %s" % type(tag))
        return tag_v

    def _extract_format_str(self, elem):
        format_str = elem.arguments[1]
        if type(format_str) is Literal:
            return format_str.value
        return None

    def extract_arguments(self, elem):
        tag_v = self._extract_tag_value(elem)
        format_str = None
        arguments = []
        if len(elem.arguments) == 2:
            format_str= self._extract_format_str(elem)
        if len(elem.arguments) > 2:
            format_str = self._extract_format_str(elem)
        return tag_v, format_str


if __name__ == "__main__":
    parser = parser.Parser()
    tree = parser.parse_file("java_src/MainActivity.java")
    tree.accept(TagVisitor(True))
