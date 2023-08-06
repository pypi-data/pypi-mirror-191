#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.
"""

from unittest import TestCase, main
from pathlib import Path
from subprocess import run

from stemplate.core import feature
from stemplate.main import command1, command2

directory = Path(__file__).parent

class TestCore(TestCase):

    def test_content(self):
        content = feature.get_beginning(directory/'data.txt')
        self.assertEqual("There is not data here.\n", content)

    def test_size(self):
        size = feature.get_size(directory/'data.txt')
        self.assertEqual(24, size)

class TestMain(TestCase):

    def test_command1(self):
        command1.main(dir=directory, file='data.txt')

    def test_command2(self):
        command2.main()

class TestCommandLineInterface(TestCase):

    def test_help(self):
        run("stemplate --help", shell=True, check=True)
        run("stemplate command1 --help", shell=True, check=True)
        run("stemplate command2 --help", shell=True, check=True)

if __name__ == '__main__':
    main()
