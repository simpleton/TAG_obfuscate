#!/usr/bin/env python

import parser
from model import *


def find_log_method(elems):
    for elem in elems:
        if type(elem) is MethodInvocation:
            if type(elem.target) is Name and elem.target.value == "Log":
                tag, format_str, params = extract_arguments(elem)
                print tag, format_str, params

def _extract_tag_value(elem):
    tag = elem.arguments[0]
    if type(tag) is Name:
        tag_v = tag.value
    elif type(tag) is Literal:
        tag_v = tag.value
    else:
        raise Exception("tag type error: %s", type(tag))
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
        for elem1 in elem.body:
            if type(elem1) is MethodDeclaration:
                find_log_method(elem1.body)
"""
                for elem2 in elem1.body:
                    if type(elem2) is MethodInvocation:
                        if type(elem2.target) is Name:
                            print elem2.name
                            print elem2.target.value
                            print elem2.arguments
                            if len(elem2.arguments) == 2:
                                tag = elem2.arguments[0]
                                if type(tag) is Name:
                                    print tag.value
                            if len(elem2.arguments) == 3:
                                tag = elem2.arguments[0]
                                if type(tag) is Name:
                                    print tag.value

if type(elem1) is FieldDeclaration:
                for elem2 in elem1.variable_declarators:
                    if elem2.variable.name.startswith("TAG"):
                        print elem2.initializer.value
"""
