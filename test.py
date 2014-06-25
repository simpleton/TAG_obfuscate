#!/usr/bin/env python

import parser
from model import *

g_var2value = {}

class Node(object):
    def __init__(self, name, father):
        self.name = name
        self.father = father
        self.key = ""
        node = self
        while node != None:
            self.key = ".".join([node.name,self.key])
            node = node.father

def get_value(var, domain):
    # use string literal as tag
    if var.startswith('\"'):
        return var

    global g_var2value
    key = "".join([domain.key, var])
    if key in g_var2value:
        return g_var2value.get(key)
    elif domain.father != None:
        return get_value(var, domain.father)
    else:
        raise Exception("can not find value in source code: %s" % var)

def parse_type_value(elems, domain):
    global g_var2value
    for elem in elems:
        if type(elem) is FieldDeclaration or type(elem) is VariableDeclaration:
            for var_dec in elem.variable_declarators:
                if type(var_dec.initializer) is Literal:
                    g_var2value["".join([domain.key, var_dec.variable.name])] = var_dec.initializer.value

def find_log_method(method_elems, domain):
    parse_type_value(method_elems, domain)
    for elem in method_elems:
        if type(elem) is MethodInvocation:
            if type(elem.target) is Name and elem.target.value == "Log":
                tag, format_str, params = extract_arguments(elem)
                tag_v = get_value(tag, domain)
                print tag_v, format_str, params

def _extract_tag_value(elem):
    tag = elem.arguments[0]
    if type(tag) is Name:
        tag_v = tag.value
    elif type(tag) is Literal:
        tag_v = tag.value
    else:
        raise Exception("tag type error: %s" % type(tag))
    return tag_v

def _extract_format_str(elem):
    format_str = elem.arguments[1]
    if type(format_str) is Literal:
        return format_str.value

def extract_arguments(elem):
    tag_v = _extract_tag_value(elem)
    format_str = None
    arguments = []
    if len(elem.arguments) == 2:
        format_str= _extract_format_str(elem)
    if  len(elem.arguments) > 2:
        format_str = _extract_format_str(elem)
        for arg in elem.arguments[2:]:
            if type(arg) is Name:
                arguments.append(arg.value)
            else:
                print type(arg)
    return tag_v, format_str, arguments

def parse_class_body(body, father):
    for elem1 in body:
        if type(elem1) is MethodDeclaration:
            node = Node(elem1.name, father)
            find_log_method(elem1.body, node)
        elif type(elem1) is ClassDeclaration:
            node = Node(elem1.name, father)
            parse_type_value(elem1.body, node)
            parse_class_body(elem1.body, node)

if __name__ == "__main__":
    parser = parser.Parser()

    tree = parser.parse_file(file('./java_src/MainActivity.java'))
    for elem in tree.type_declarations:
        # parse all type declaration's value
        root = Node(elem.name, None)
        parse_type_value(elem.body, root)
        parse_class_body(elem.body, root)
