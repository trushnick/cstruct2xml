#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from enum import Enum

class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

class TokenType(Enum):
    pass