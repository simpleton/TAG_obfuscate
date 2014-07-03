#!/usr/bin/env python

import parser
from TagVisitor import TagVisitor
from model import *
from Tag import Tag
from Node import Node

DEBUG = False

def _print( *params ):
    if DEBUG:
        print params

class TagParser(object):
    def __init__(self, source_parser=parser.Parser()):
        self.var2value = {}
        self.tags = []
        self.format_strs = []
        self.source_parser = source_parser
        self.visitor = TagVisitor()


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
            return None
#            raise Exception("can not find value in source code: %s" % var)

    def parse_type_value(self, elems, domain):
        """
        parse type value
        """
        for elem in elems:
            if type(elem) is FieldDeclaration or type(elem) is VariableDeclaration:
                for var_dec in elem.variable_declarators:
                    if type(var_dec.initializer) is Literal:
                        self.var2value["".join([domain.key, var_dec.variable.name])] = var_dec.initializer.value
        return ;


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
                    #FIXME: ignore didn't init TAG's value
                    if tag_v == None:
                        continue

                    tag = Tag(tag_k, tag_v)
                    if tag not in self.tags:
                        self.tags.append(tag)
                    _print(tag_v, format_str)
        return;

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

        return ;

    def parse(self, file):
        _print( file )
        tree = self.source_parser.parse_file(file)
        tree.accept(self.visitor)
        return self.visitor.tags


if __name__ == "__main__":
    tag_parser = TagParser()
    for e in tag_parser.parse(file('./java_src/MainActivity.java')):
        print e
