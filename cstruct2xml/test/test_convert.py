#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from xml.etree import ElementTree as ET
from cstruct2xml.parser import Structure, Variable
from cstruct2xml.convert import convert


class TestConvert(unittest.TestCase):

    def test_convert(self):
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

        xml = convert(structure)
        root = ET.fromstring(xml)
        self.assertEqual(root.tag, 'structure')

        name = root.find('name')
        self.assertEqual(name.text, structure.name)

        description = root.find('description')
        self.assertEqual(description.text, structure.description)

        variables = root.find('variables')
        self.assertEqual(len(variables), len(structure.variables))

    def test_convert_file(self):
        # TODO: 
        pass
