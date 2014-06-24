#!/usr/bin/env python

import parser
from model import *

g_var2value = {}

def get_value(var):
    # use string literal as tag
    if var.startswith('\"'):
        return var

    global g_var2value
    if var in g_var2value:
        return g_var2value.get(var)
    else:
        raise Exception("can not find value in source code: %s" % var)

def parse_type_value(elems):
    global g_var2value
    for elem in elems :
        if type(elem) is FieldDeclaration:
            for var_dec in elem.variable_declarators:
                if type(var_dec.initializer) is Literal:
                    g_var2value[var_dec.variable.name] = var_dec.initializer.value

def find_log_method(method_elems):
    for elem in method_elems:
        if type(elem) is MethodInvocation:
            if type(elem.target) is Name and elem.target.value == "Log":
                tag, format_str, params = extract_arguments(elem)
                tag_v = get_value(tag)
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


if __name__ == "__main__":
    parser = parser.Parser()

    tree = parser.parse_file(file('./java_src/MainActivity.java'))
    for elem in tree.type_declarations:
        # parse all type declaration's value
        parse_type_value(elem.body)
        for elem1 in elem.body:
            if type(elem1) is MethodDeclaration:
                find_log_method(elem1.body)
