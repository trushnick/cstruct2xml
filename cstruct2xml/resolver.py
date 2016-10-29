#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lxml.etree as et
from io import StringIO
import copy


def resolve(xml, defines):
    """
    Runs through xml checking all <type> and <array_size> tags.
    If type or array size is unresolved, it tries to resolve it.
    Generally, if there is unresolved reference in type, it will look up for the structure with this name and replace
    variable tag with structure tag.
    For array_size, if there would be not decimal number, it will try to make it so. If there would be variable name,
    it will look up in the defines for the value. If there is binary/octal/hex number, it will convert it to decimal.
    :param xml: Generated xml for one file (either root element or str)
    :param defines: Dict of defines from file in format alias:value
    :return: Transformed xml with resolved types and sizes (str)
    """
    parser = et.XMLParser(remove_blank_text=True)
    if isinstance(xml, str):
        buffer = StringIO(xml)
        xml = et.parse(buffer, parser)
    structure_names = {structure_obj.find('name').text: structure_obj
                       for structure_obj in xml.iterfind('structure')}
    # Type resolving
    for var in xml.iterfind('structure/variables/variable'):
        var_type = var.find('type').text
        if var_type in structure_names.keys():
            var_name = var.find('name').text
            var_array_size = var.find('array_size').text
            var_description = var.find('description').text
            structure_element = copy.deepcopy(structure_names[var_type])
            structure_element.find('name').text = var_name
            structure_element.find('description').text = var_description
            array_size = et.Element('array_size')
            array_size.text = str(var_array_size)
            structure_element.insert(2, array_size)
            var.getparent().replace(var, structure_element)
    # Array size resolving
    for var in xml.iterfind('structure/variables/'):
        array_size = var.find('array_size').text
        if array_size in defines.keys():
            var.find('array_size').text = str(defines[array_size])
    return et.tostring(xml, encoding='unicode', pretty_print=True)
