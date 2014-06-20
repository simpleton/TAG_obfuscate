#!/usr/bin/env python

import parser
from model import *

if __name__ == "__main__":
    parser = parser.Parser()

    tree = parser.parse_file(file('./java_src/MainActivity.java'))
    for elem in tree.type_declarations:
        for elem1 in elem.body:
            if type(elem1) is MethodDeclaration:
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
