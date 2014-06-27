#!/usr/bin/env python

import parser
from model import *

DEBUG = False

class Node(object):
    def __init__(self, name, father):
        self.name = name
        self.father = father
        self.key = ""
        node = self
        while node != None:
            self.key = ".".join([node.name,self.key])
            node = node.father

class Tag(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

class TagParser(object):
    def __init__(self, source_parser=parser.Parser()):
        self.var2value = {}
        self.tags = []
        self.format_strs = []
        self.source_parser = source_parser
        self.log_method_list = ['i', 'd', 'e', 'v', 'f', 'w', 'printDebugStack', 'printInfoStack', 'printErrStackTrace']

    def get_value(self, var, domain):
        # use string literal as tag
        if var.startswith('\"'):
            return var

        key = "".join([domain.key, var])
        if key in self.var2value:
            return self.var2value.get(key)
        elif domain.father != None:
            return self.get_value(var, domain.father)
        else:
            raise Exception("can not find value in source code: %s" % var)

    def parse_type_value(self, elems, domain):
        for elem in elems:
            if type(elem) is FieldDeclaration or type(elem) is VariableDeclaration:
                for var_dec in elem.variable_declarators:
                    if type(var_dec.initializer) is Literal:
                        self.var2value["".join([domain.key, var_dec.variable.name])] = var_dec.initializer.value

    def find_log_method(self, method_elems, domain):
        self.parse_type_value(method_elems, domain)
        for elem in method_elems:
            if type(elem) is MethodInvocation:
                if type(elem.target) is Name and elem.target.value == "Log" and elem.name in self.log_method_list:
                    tag_k, format_str = self.extract_arguments(elem)

                    #FIXME: didn't support reference other class's tag
                    if '.' in tag_k:
                        continue

                    tag_v = self.get_value(tag_k, domain)
                    tag = Tag(tag_k, tag_v)
                    if tag not in self.tags:
                        self.tags.append(tag)
                    if DEBUG:
                        print tag_v, format_str

    def _extract_tag_value(self, elem):
        if hasattr(elem , 'arguments'):
            print elem.arguments
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

    def extract_arguments(self, elem):
        tag_v = self._extract_tag_value(elem)
        format_str = None
        arguments = []
        if len(elem.arguments) == 2:
            format_str= self._extract_format_str(elem)
        if len(elem.arguments) > 2:
            format_str = self._extract_format_str(elem)
        return tag_v, format_str

    def parse_class_body(self, body, father):
        for elem1 in body:
            if hasattr(elem1, 'body') and elem1.body == None:
                continue

            if type(elem1) is MethodDeclaration:
                node = Node(elem1.name, father)
                self.find_log_method(elem1.body, node)

            elif type(elem1) is ClassDeclaration:
                node = Node(elem1.name, father)
                self.parse_type_value(elem1.body, node)
                self.parse_class_body(elem1.body, node)

    def parse(self, file):
        print file
        tree = self.source_parser.parse_file(file)
        for elem in tree.type_declarations:
            # parse all type declaration's value
            if hasattr(elem, 'name'):
                root = Node(elem.name, None)
                self.parse_type_value(elem.body, root)
                self.parse_class_body(elem.body, root)
        return self.tags

if __name__ == "__main__":
    tag_parser = TagParser()
    for e in tag_parser.parse(file('./java_src/MainActivity.java')):
        print e
