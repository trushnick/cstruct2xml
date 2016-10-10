#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .tokens import Token, TokenType
from .lexer import Lexer


class Structure:

    def __init__(self):
        self.name = ''
        self.description = ''
        self.variables = []

    def add_variable(self, variable):
        self.variables.append(variable)


class Variable:

    def __init__(self):
        self.description = None
        self.type = None
        self.value = None
        self.array_size = None


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current = next(lexer)
        self.structure = Structure()
        self.current_var = None

    def parse(self):
        return self._structure_definition()

    def _struct_def(self):
        # struct_def -> comment_block TYPEDEF STRUCT LCB struct_body RCB struct_name SC
        self.structure.description = self._comment_block()
        self._match(TokenType.TYPEDEF)
        self._match(TokenType.STRUCT)
        self._match(TokenType.LCB)
        self._structure_body(self.structure)
        self._match(TokenType.RCB)
        self.structure.name = self._structure_name()
        self._match(TokenType.SC)
        return self.structure

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
            self.current = next(self.lexer)
        return comment_block.strip()

    def _struct_body(self, structure):
		# struct_body ->	stuct_body struct_member | 
		#					struct_member
		# Getting rid of left recursion:
		# struct_body ->	struct_member struct_body2
		# struct_body2->	struct_member struct_body2 | %empty%
        current_var = self._struct_member()
		structure.variables.append(current_var)
		while self.current.type not in [TokenType.RCB]:
			current_var = self._struct_member()
			structure.variables.append(current_var)

	def _struct_member(self):
		# struct_member ->	inner_struct_def |
		#					var_decl
		description = self._comment_block()
		variable = None
		if self.current.type == TokenType.STRUCT:
			variable = self._inner_structure()
			variable.value.description = desription
		else:
			variabletructure()
            variable.value.description = desription
        else:
            variable = self._var_decl()
        variable.description = description
        return variable

    def _inner_struct_def(self):
        # inner_struct_def -> comment_block STRUCT RCB struct_body RCB struct_name SC
        # comment_block read in struct_member()
        current_var = Variable()
        current_var.type = 'struct'
        current_var.array_size = 1
        current_var.value = Structure()
        # place of comment block, already read outside this function, so no need to read again  
        self._match(TokenType.STRUCT)
        self._match(TokenType.LCB)
		variable.description = description
		return variable

    def _inner_struct_def(self):
        # inner_struct_def -> comment_block STRUCT RCB struct_body RCB struct_name SC
        # comment_block read in struct_member()
		current_var = Variable()
        current_var.type = 'struct'
        current_var.array_size = 1
		current_var.value = Structure()
		# place of comment block, already read outside this function, so no need to read again
        self._match(TokenType.STRUCT)
        self._match(TokenType.LCB)
        self._structure_body(current_var.value)
        self._match(TokenType.RCB)
        current_var.name = current_var.value.name = self._struct_name()
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
				self._match(VARIABLE_NAME).value,
				1 if self.current.type == TokenType.SC else self._array_size())
		self._match(TokenType.SC)
		return spec

    def _var_type(self):
		# var_type ->	prim_type |
		#				users_type
		# users_type -> VARIABLE_NAME
        type = ''
		if self.current.type == TokenType.VARIABLE_NAME:
			t = self._match(TokenType.VARIABLE_NAME)
			type = t.value
		else
			type = self._prim_type()
		return type

    def _prim_type(self):
        # prim_type -> int_type | float_type
		# int_type -> 	sign_mod |
		#				sign_mod INT |
		#				size_mod |
		#				size_mod INT |
		#				sign_mod size_mod |
		#				sign_mod size_mod INT |
		#				sign_mod CHAR |
		#				CHAR | 
		#				INT
		# float_type ->	FLOAT | DOUBLE | LONG DOUBLE
		# TODO: REFACTOR, code duplicates
		type = []
		if self.current.type in [TokenType.UNSIGNED, TokenType.SIGNED]:
			if self.current.type == TokenType.SIGNED:
				type.append(self._match(TokenType.SIGNED).value)
			else
				type.append(self._match(TokenType.UNSIGNED).value)
			if self.current.type == TokenType.CHAR:
				type.append(self._match(TokenType.CHAR).value)
			elif self.current.type in [TokenType.SHORT, TokenType.LONG]:
				if self.current.type == TokenType.SHORT:
					type.append(self._match(TokenType.SHORT).value)
				else:
					type.append(self._match(TokenType.LONG).value)
					if self.current.type == TokenType.LONG:
						type.append(self._match(TokenType.LONG).value)
				if self.current.type == TokenType.INT:
					type.append(self._match(TokenType.INT).value)
			elif self.current.type == TokenType.INT:
				type.append(self._match(TokenType.INT).value)
		elif self.current.type in [TokenType.SHORT, TokenType.LONG]:
			if self.current.type == TokenType.SHORT:
                    type.append(self._match(TokenType.SHORT).value)
                else:
                    type.append(self._match(TokenType.LONG).value)
                    if self.current.type == TokenType.LONG:
                        type.append(self._match(TokenType.LONG).value)
					elif self.current.type == TokenType.DOUBLE:
						type.append(self._match(TokenType.DOUBLE).value)
            if self.current.type == TokenType.INT:
                type.append(self._match(TokenType.INT).value)
		elif self.current.type == TokenType.INT:
			type.append(self._match(TokenType.INT).value)
		elif self.current.type == TokenType.FLOAT:
			type.append(self._match(TokenType.FLOAT).value)
		elif self.current.type == TokenType.DOUBLE:
			type.append(self._match(TokenType.DOUBLE).value)
		else:
			type.append(self._match(TokenType.CHAR).value)
		return ' '.join(type)			


    def _array_specifier(self):
        self._match(TokenType.LSB)
		self._array_size_expr()
		self._match(TokenType.RSB)

    def _array_size_expr(self):
        # array_size_expr ->	array_size_expr2 PLUS array_size_expr |
		#						array_size_expr2 MINUS array_size_expr |
		#						array_size_expr2
		expr = self._array_size_expr2()
		if self.current.type in [TokenType.PLUS, TokenType.MINUS]:
			if self.current.type == TokenType.PLUS:
				expr += self._match(TokenType.PLUS).value)
			else:
				expr += self._match(TokenType.MINUS).value)
			expr += self._array_size_expr()

    def _array_size_expr2(self):
        # array_size_expr2 ->	array_size_expr3 MUL array_size_expr2 |
		#						array_size_expr3 DIV array_size_expr2 |
		#						array_size_expr3 
		expr = self._array_size_expr3()
		if self.current.type in [TokenType.DIV, TokenType.MUL]:
            if self.current.type == TokenType.MUL:
                expr += self._match(TokenType.MUL).value)
            else:
                expr += self._match(TokenType.DIV).value)
            expr += self._array_size_expr2()

    def _array_size_expr3(self):
        # array_size_expr3 ->	LB array_size_expr RB |
		#						NUMBER |
		#						VARIABLE_NAME
		if self.current.type == TokenType.NUMBER:
			expr = self._match(TokenType.NUMBER).value
		elif self.current.type == TokenType.VARIABLE_NAME:
			expr = self._match(TokenType.VARIABLE_NAME).value
		else:
			expr = self._match(TokenType.LB).value
			expr += self._array_size_expr()
			epxr += self._match(TokenType.RB).value
		return expr

    def _struct_name(self):
        # struct_name -> VARIABLE_NAME
        t = self._match(TokenType.VARIABLE_NAME)
        return t.value

    def _match(self, types):
		# TODO: reconsider, maybe return token.value instead of token? (check usages)
        if self.current.type in types:
            token = self.current
            self.current = next(self.lexer)
            return token
        else:
            raise ParserError(self.current, self.lexer.line_number, self.lexer.line_pos)


class ParserError(Exception):

    def __init__(self, token, line_number, line_pos):
        message = 'Wrong lexeme: {} at line {}, pos {}'.format(token, line_number, line_pos)
        super(ParserError, self).__init__(message)
