#!/usr/bin/env python2
import model as m
import parser
import sys


class MyVisitor(m.Visitor):

    def __init__(self):
        super(MyVisitor, self).__init__()

        self.first_field = True
        self.first_method = True


    def visit_ClassDeclaration(self, class_decl):
        return self.visit_type_declaration(class_decl)

    def visit_InterfaceDeclaration(self, interface_decl):
        return self.visit_type_declaration(interface_decl)


    def visit_type_declaration(self, type_decl):
        print(str(type_decl.name))
        if type_decl.extends is not None:
            print type_decl.extends
        if hasattr(type_decl, "implements") and  len(type_decl.implements) is not 0:
            print(' -> implementing ' + ', '.join([type.name.value for type in type_decl.implements]))
        print

        return True

    def visit_FieldDeclaration(self, field_decl):
        if self.first_field:
            print('fields:')
            self.first_field = False
        for var_decl in field_decl.variable_declarators:
            if type(field_decl.type) is str:
                type_name = field_decl.type
            else:
                type_name = field_decl.type.name.value
            print('    ' + type_name + ' ' + var_decl.variable.name)


    def visit_VariableDeclaration(self, var_declaration):
        for var_decl in var_declaration.variable_declarators:
            if type(var_declaration.type) is str:
                type_name = var_declaration.type
            else:
                type_name = var_declaration.type.name.value
            print('        ' + type_name + ' ' + var_decl.variable.name)

    def visit_MethodInvocation(self, invoke_decl):
        print invoke_decl

if __name__ == "__main__":
    parser = parser.Parser()
    tree = parser.parse_file("java_src/test.java")
    tree.accept(MyVisitor())
