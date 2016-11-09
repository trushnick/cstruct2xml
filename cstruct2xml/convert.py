#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import lxml.etree as ET
from xml.dom import minidom


def convert_file(name, structures):
    file = ET.Element('file', {'name':name})
    for structure in structures:
        file.append(_convert_structure(structure))
    return file


def convert(structure):
    return _convert_structure(structure)


def _convert_structure(structure, count = 0):
    struct = ET.Element('structure')

    name = ET.Element('name')
    name.text = structure.name
    struct.append(name)

    description = ET.Element('description')
    description.text = structure.description
    struct.append(description)

    if count:
        array_size = ET.Element('array_size')
        array_size.text = str(count)
        struct.append(array_size)

    variables = ET.Element('variables')
    for v in structure.variables:
        v_element = _convert_variable(v)
        variables.append(v_element)
    struct.append(variables)

    return struct


def _convert_variable(variable):

    if variable.type == 'struct':
        var_el = _convert_structure(variable.value, variable.array_size)
    else:
        var_el = ET.Element('variable')

        name = ET.Element('name')
        name.text = variable.value

        type = ET.Element('type')
        type.text = variable.type

        description = ET.Element('description')
        description.text = variable.description

        array_size = ET.Element('array_size')
        array_size.text = str(variable.array_size)

        var_el.append(name)
        var_el.append(type)
        var_el.append(description)
        var_el.append(array_size)
    return var_el


def _prettify(top_element):
    return ET.tostring(top_element, encoding='unicode', pretty_print=True)
