#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lxml


def resolve(xml, defines):
    """
    Runs through xml checking all <type> and <array_size> tags.
    If type or array size is unresolved, it tries to resolve it.
    Generally, if there is unresolved reference in type, it will look up for the structure with this name and replace
    variable tag with structure tag.
    For array_size, if there would be not decimal number, it will try to make it so. If there would be variable name,
    it will look up in the defines for the value. If there is binary/octal/hex number, it will convert it to decimal.
    :param xml: Either ElementTree or string, representing xml for one file
    :param defines: Dict of defines from file in format alias:value
    :return: Transformed xml with resolved types and sizes.
    """
    # TODO: Also try to interpret array size
    pass