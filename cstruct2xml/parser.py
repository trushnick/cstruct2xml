#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .tokens import TokenType

# Sign mods for primitive int types
_sign_mods = [TokenType.SIGNED, TokenType.UNSIGNED]
# Size mods for primitive int types
_size_mods = [TokenType.SHORT, TokenType.LONG]
# Mapping between types in declaration and type group
_type_groups = {
    # Char types -> char
    'char': 'char',
    'signed char': 'char',
    'unsigned char': 'char',
    # Short types
    # Signed -> short
    # Unsigneds -> ushort
    'short': 'short',
    'short int': 'short',
    'signed short': 'short',
    'signed short int': 'short',
    'unsigned short': 'ushort',
    'unsigned short int': 'ushort',
    # Ints
    # Signed -> int
    # Unsigned -> uint
    'int': 'int',
    'signed': 'int',
    'signed int': 'int',
    'unsigned': 'uint',
    'unsigned int': 'uint',
    # Longs
    # Signed -> long
    # Unsigned -> ulong
    'long': 'long',
    'long int': 'long',
    'signed long': 'long',
    'signed long int': 'long',
    'unsigned long': 'ulong',
    'unsigned long int': 'ulong',
    # Long longs
    # Signed -> llong
    # Unsigned -> ullong
    'long long': 'llong',
    'long long int': 'llong',
    'signed long long': 'llong',
    'signed long long int': 'llong',
    'unsigned long long': 'ullong',
    'unsigned long long int': 'ullong',
    # Float
    'float': 'float',
    # Double, long double
    'double': 'double',
    'long double': 'ldouble'
}


class Structure:

    def __init__(self):
        self.name = None
        self.description = None
        self.variables = []


class Variable:

    def __init__(self):
        self.description = None
        self.type = None
        self.value = None
        self.array_size = None


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.lexer_iter = iter(lexer)
        self.current = next(self.lexer_iter)
        self.structure = Structure()
        self.current_var = None

    def parse(self):
        return self._struct_def()

    def _struct_def(self):
        # struct_def -> comment_block TYPEDEF? STRUCT struct_name1? LCB struct_body RCB struct_name SC
        self.structure.description = self._comment_block()
        if self.current.type == TokenType.TYPEDEF:
            self._match(TokenType.TYPEDEF)
        self._match(TokenType.STRUCT)
        if self.current.type == TokenType.VARIABLE_NAME:
            self.structure.name = self._match(TokenType.VARIABLE_NAME)
        self._comment_block()  # Skipping comments before opening bracket
        self._match(TokenType.LCB)
        self._struct_body(self.structure)
        self._comment_block()  # Skipping comment before closing bracket
        self._match(TokenType.RCB)
        if not self.structure.name:
            self.structure.name = self._struct_name()
        else:
            self._struct_name()
        try:
            self._match(TokenType.SC)
        except ParserError as e:
            if e.message.startswith("Wrong"):
                raise e
            else:
                return self.structure
        else:
            raise ParserError("End of lexemes expected, but {} found".format(
                self.current))

    def _comment_block(self):
        # comment_block -> comment_block comment | comment | %empty%
        comment_block = ''
        while self.current.type in [TokenType.END_OF_LINE_COMMENT, TokenType.TRADITIONAL_COMMENT]:
            comment = self.current.value[2:]
            if self.current.type == TokenType.TRADITIONAL_COMMENT:
                comment = comment[:-2]
                comment = '\n'.join(line.strip() for line in comment.split('\n'))
            else:
                comment = comment.strip()
            comment_block += '\n' + comment
            self.current = next(self.lexer_iter)
        return comment_block.strip()

    def _struct_body(self, structure):
        # struct_body ->    stuct_body struct_member |
        #                   struct_member
        # Getting rid of left recursion:
        # struct_body ->    struct_member struct_body2
        # struct_body2->    struct_member struct_body2 | %empty%
        current_var = self._struct_member()
        while self.current.type != TokenType.RCB and current_var is not None:
            structure.variables.append(current_var)
            current_var = self._struct_member()
        if current_var is not None:
            structure.variables.append(current_var)

    def _struct_member(self):
        # struct_member ->  inner_struct_def |
        #                   var_decl
        description = self._comment_block()
        if self.current.type == TokenType.RCB:  # Comment block before closing bracket of structure
            return None
        elif self.current.type == TokenType.STRUCT:
            variable = self._inner_struct_def()
            variable.value.description = description
        else:
            variable = self._var_decl()
        variable.description = description
        return variable

    def _inner_struct_def(self):
        # inner_struct_def -> comment_block STRUCT RCB struct_body RCB struct_name SC
        # comment_block read in struct_member()
        current_var = Variable()
        current_var.type = 'struct'
        current_var.value = Structure()
        # place of comment block, already read outside this function, so no need to read again
        self._match(TokenType.STRUCT)
        if self.current.type == TokenType.VARIABLE_NAME:
            current_var.value.name = self._match(TokenType.VARIABLE_NAME)
        self._comment_block()  # Skipping comment block before opening bracket
        self._match(TokenType.LCB)
        self._struct_body(current_var.value)
        self._comment_block()  # Skipping comment block before closing bracket
        self._match(TokenType.RCB)
        current_var.name = current_var.value.name = self._match(TokenType.VARIABLE_NAME)
        current_var.array_size = 1 if self.current.type != TokenType.LSB else self._array_specifier()
        self._match(TokenType.SC)
        return current_var

    def _var_decl(self):
        # var_decl -> comment_block var_spec
        # comment_block read in struct_member()
        current_var = Variable()
        current_var.type, current_var.value, current_var.array_size = self._var_spec()
        return current_var

    def _var_spec(self):
        # var_spec -> var_type VARIABLE_NAME SC |
        #             var_type VARIABLE_NAME array_specifier SC
        spec = (self._var_type(),
                self._match(TokenType.VARIABLE_NAME),
                1 if self.current.type == TokenType.SC else self._array_specifier())
        self._match(TokenType.SC)
        return spec

    def _var_type(self):
        # var_type ->    prim_type |
        #                users_type
        # users_type -> VARIABLE_NAME
        if self.current.type == TokenType.VARIABLE_NAME:
            var_type = self._match(TokenType.VARIABLE_NAME)
        else:
            var_type = self._prim_type()
        return var_type

    def _prim_type(self):
        # prim_type -> int_type | float_type
        # int_type ->     sign_mod |
        #                sign_mod INT |
        #                size_mod |
        #                size_mod INT |
        #                sign_mod size_mod |
        #                sign_mod size_mod INT |
        #                sign_mod CHAR |
        #                CHAR |
        #                INT
        # float_type ->    FLOAT | DOUBLE | LONG DOUBLE
        # TODO: REFACTOR, code duplicates
        var_type = []
        if self.current.type == TokenType.DOUBLE:
            var_type.append(self._match(TokenType.DOUBLE))
        elif self.current.type == TokenType.FLOAT:
            var_type.append(self._match(TokenType.FLOAT))
        else:
            if self.current.type in _sign_mods:
                if self.current.type == TokenType.SIGNED:
                    var_type.append(self._match(TokenType.SIGNED))
                else:
                    var_type.append(self._match(TokenType.UNSIGNED))
            if self.current.type == TokenType.CHAR:
                var_type.append(self._match(TokenType.CHAR))
            else:
                if self.current.type in _size_mods:
                    if self.current.type == TokenType.SHORT:
                        var_type.append(self._match(TokenType.SHORT))
                    else:
                        var_type.append(self._match(TokenType.LONG))
                        if self.current.type == TokenType.LONG:
                            var_type.append(self._match(TokenType.LONG))
                        elif self.current.type == TokenType.DOUBLE:
                            var_type.append(self._match(TokenType.DOUBLE))
                            return _type_groups[' '.join(var_type)]  # Returning earlier because it's specific
                if self.current.type == TokenType.INT:
                    var_type.append(self._match(TokenType.INT))
        return _type_groups[' '.join(var_type)]

    def _array_specifier(self):
        # array_specifier ->    LSB array_size_expr RSB
        self._match(TokenType.LSB)
        expr = self._array_size_expr()
        self._match(TokenType.RSB)
        return expr

    def _array_size_expr(self):
        # array_size_expr ->    array_size_expr2 PLUS array_size_expr |
        #                        array_size_expr2 MINUS array_size_expr |
        #                        array_size_expr2
        expr = self._array_size_expr2()
        if self.current.type in [TokenType.PLUS, TokenType.MINUS]:
            if self.current.type == TokenType.PLUS:
                expr += self._match(TokenType.PLUS)
            else:
                expr += self._match(TokenType.MINUS)
            expr += self._array_size_expr()
        return expr

    def _array_size_expr2(self):
        # array_size_expr2 ->    array_size_expr3 MUL array_size_expr2 |
        #                        array_size_expr3 DIV array_size_expr2 |
        #                        array_size_expr3
        expr = self._array_size_expr3()
        if self.current.type in [TokenType.DIV, TokenType.MUL]:
            if self.current.type == TokenType.MUL:
                expr += self._match(TokenType.MUL)
            else:
                expr += self._match(TokenType.DIV)
            expr += self._array_size_expr2()
        return expr

    def _array_size_expr3(self):
        # array_size_expr3 ->    LB array_size_expr RB |
        #                        NUMBER |
        #                        VARIABLE_NAME
        if self.current.type == TokenType.NUMBER:
            expr = self._match(TokenType.NUMBER)
        elif self.current.type == TokenType.VARIABLE_NAME:
            expr = self._match(TokenType.VARIABLE_NAME)
        else:
            expr = self._match(TokenType.LB)
            expr += self._array_size_expr()
            expr += self._match(TokenType.RB)
        return expr

    def _struct_name(self):
        # struct_name -> VARIABLE_NAME
        return self._match(TokenType.VARIABLE_NAME)

    def _match(self, ttype):
        if self.current.type == ttype:
            token = self.current
            try:
                self.current = next(self.lexer_iter)
            except StopIteration:
                raise ParserError("{} expected, but end of lexemes found".format(ttype))
            return token.value
        else:
            message = "Wrong lexeme {} at line {}, pos {}. {} expected".format(
                self.current, self.lexer.line_number, self.lexer.line_pos, ttype)
            raise ParserError(message)


class ParserError(Exception):

    def __init__(self, message="Unknown message"):
        self.message = message
        super(ParserError, self).__init__(message)
