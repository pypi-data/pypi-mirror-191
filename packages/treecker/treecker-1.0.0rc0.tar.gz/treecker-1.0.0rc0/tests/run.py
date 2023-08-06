#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.
"""

from unittest import TestCase, main
from pathlib import Path

from treecker.core import tree, snapshot, naming, configuration, comparison

directory = Path(__file__).parent / 'dir'

class TestCore(TestCase):

    def test_hash(self):
        hash = tree.file_hash(directory/'file.txt')
        self.assertEqual(hash, '6c636eca9b4df0f8244ed6e9ad37517c')

    def test_size(self):
        size = tree.file_size(directory/'file.txt')
        self.assertEqual(size, 52)

if __name__ == '__main__':
    main()
