#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.parser import Structure, Variable
from lib.convert import convert


def test_convert():
    structure = Structure()
    structure.name = "SampleStructure"
    structure.description = "Description of structure\nMade for testing"

    var1 = Variable()
    var1.type = 'int'
    var1.value = 'foo'
    var1.description = 'var 1 description'
    var1.array_size = '1'

    var2 = Variable()
    var2.type = 'int'
    var2.value = 'foo'
    var2.description = 'var 1 description'
    var2.array_size = '1'

    var3 = Variable()
    var3.type = 'int'
    var3.value = 'foo'
    var3.description = 'var 1 description'
    var3.array_size = '1'

    var4 = Variable()
    var4.type = 'int'
    var4.value = 'foo'
    var4.description = 'var 1 description'
    var4.array_size = '1'

    structure.variables.append(var1)
    structure.variables.append(var2)
    structure.variables.append(var3)
    structure.variables.append(var4)

    root = convert(structure)
    # root = ET.fromstring(xml)
    assert root.tag == 'structure'

    name = root.find('name')
    assert name.text == structure.name

    description = root.find('description')
    assert description.text, structure.description

    variables = root.find('variables')
    assert len(variables) == len(structure.variables)

def test_convert_file():
    # TODO:
    pass
