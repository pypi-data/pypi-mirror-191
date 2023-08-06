#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.
"""

from unittest import TestCase, main
from pathlib import Path
from os import remove
from subprocess import run

from treecker.core import tree, snapshot, naming, configuration, comparison
from treecker.main import init, status, commit, issues

directory = Path(__file__).parent / 'dir'

class TestCore(TestCase):

    def test_file_hash(self):
        hash = tree.file_hash(directory/'file.txt')
        self.assertEqual('6c636eca9b4df0f8244ed6e9ad37517c', hash)

    def test_file_size(self):
        size = tree.file_size(directory/'file.txt')
        self.assertEqual(52, size)

    def test_node_no_hash(self):
        node = tree.tree_node(directory, [], False)
        stored = {
            'file.txt': [52],
            'subdir': {
                'setup.sh': [49],
            },
        }
        self.assertDictEqual(stored, node)

    def test_node_hash(self):
        node = tree.tree_node(directory, ['file*'], True)
        stored = {
            'subdir': {
                'setup.sh': [49, '6f8693e997b0a35a91962bac1ad0eb72'],
            },
        }
        self.assertDictEqual(stored, node)

    def test_items(self):
        node = tree.tree_node(directory, [], False)
        items = tree.tree_items(node)
        stored = [(['file.txt'], [52]), (['subdir', 'setup.sh'], [49])]
        self.assertListEqual(stored, items)

    def test_snapshot_serialization(self):
        for hash in (True, False):
            with self.subTest(hash=hash):
                snap1 = snapshot.take(directory, hash)
                snapshot.save(directory, snap1)
                snap2 = snapshot.load(directory)
                self.assertDictEqual(snap1, snap2)
                remove(directory/'treecker.json')

    def test_naming_issues(self):
        issues = naming.issues({'UP': [10]})
        self.assertEqual(len(issues), 1)
        issues = naming.issues({'spa ce': [2]})
        self.assertEqual(len(issues), 1)
        issues = naming.issues({'a.tar.gz': [2]})
        self.assertEqual(len(issues), 0)

    def test_configuration_update(self):
        with open(directory/'treecker.conf', 'w') as file:
            file.write("[test]\nvalue = 3")
        config = dict(configuration.config)
        configuration.update(directory)
        remove(directory/'treecker.conf')
        self.assertEqual('3', configuration.config.get('test', 'value'))

    def test_differences(self):
        node1 = {'a': {'b': [2, 'h1']}, 'c': {'d': [2, 'h2']}}
        node2 = {'a': {'b': [2, 'h1']}, 'c': {'d': [2, 'h2']}}
        node3 = {'a': {'b': [2, 'h1']}}
        for hash in (True, False):
            with self.subTest(hash=hash):
                diffs = comparison.differences(node1, node2, hash)
                self.assertEqual(0, len(diffs))
                diffs = comparison.differences(node1, node3, hash)
                self.assertEqual(1, len(diffs))

class TestMain(TestCase):

    def test_init(self):
        for hash in (True, False):
            with self.subTest(hash=hash):
                init.main(dir=directory, hash=hash)
                self.assertRaises(Exception, init.main, dir=directory, hash=hash)
                remove(directory/'treecker.json')

    def test_status(self):
        init.main(dir=directory, hash=True)
        for hash in (True, False):
            with self.subTest(hash=hash):
                status.main(dir=directory, hash=hash)
        remove(directory/'treecker.json')

    def test_commit(self):
        init.main(dir=directory, hash=False)
        commit.main(dir=directory, hash=False)
        remove(directory/'treecker.json')

    def test_issues(self):
        issues.main(dir=directory)

class TestCommandLineInterface(TestCase):

    def test_help(self):
        run("treecker --help", shell=True, check=True)
        run("treecker init --help", shell=True, check=True)
        run("treecker status --help", shell=True, check=True)
        run("treecker commit --help", shell=True, check=True)
        run("treecker issues --help", shell=True, check=True)

if __name__ == '__main__':
    main()
