#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
from xml.dom import minidom


def convert(structure):
    return _prettify(_convert_structure(structure))


def _convert_structure(structure):
    struct = ET.Element('structure')
    
    name = ET.Element('name')
    name.text = structure.name

    description = ET.Element('description')    
    description.text = structure.description
    
    variables = ET.Element('variables')
    for v in structure.variables:
        v_element = _convert_variable(v)
        variables.append(v_element)

    struct.append(name)
    struct.append(description)
    struct.append(variables)
    
    return struct


def _convert_variable(variable):
    if variable.type == 'struct':
        var_el = _convert_structure(variable.value)
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
    xml = ET.tostring(top_element, 'utf-8')
    return minidom.parseString(xml).toprettyxml(indent='  ')
