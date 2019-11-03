#!/usr/bin/python
# -*- coding: utf-8 -*-
# apply-license-java.py - A simple tool to add license information to the beginning of java files
# Copyright (c) 2019, Fabio Jun Takada Chino. All rights reserved.
# This script is licensed under the termos of BSD 3-Clause License. 
# See https://github.com/fjtc/apply-license-java for further information
import unittest
import os
import os.path
import common
import tempfile
from common import FilteredTextFile
from common import FilteredJavaFile

class NoEmptyFilteredTextFile(FilteredTextFile):
    def __init__(self, file_name, encoding = 'utf-8'):
        super().__init__(file_name, encoding)

    def filter_line(self, line):
        if len(line.strip()) > 0:
            return line
        else:
            None

class FilteredTextFileTest(unittest.TestCase):

    def test_init(self):
        f = FilteredTextFile('file')
        self.assertEqual('file', f.file_name)
        self.assertEqual('utf-8', f.encoding)
        self.assertEqual([], f.contents)

        f = FilteredTextFile('file', 'iso-8859-1')
        self.assertEqual('file', f.file_name)
        self.assertEqual('iso-8859-1', f.encoding)
        self.assertEqual([], f.contents)

    def test_file_name(self):
        f = FilteredTextFile('file')
        self.assertEqual('file', f.file_name)
        f.file_name = 'file2'
        self.assertEqual('file2', f.file_name)

    def test_load(self):
        f = FilteredTextFile(os.path.join('sample', 'VersionInfoBean.java'))
        f.load()
        self.assertTrue(len(f.contents) > 0)
        self.assertEqual('package it.is.just.a.test;', f.contents[0].strip())

        f.load(os.path.join('sample', 'VersionInfoBeanLicensed.java'))
        self.assertTrue(len(f.contents) > 0)
        self.assertEqual('/*', f.contents[0].strip())

    def test_save(self):
        tmp_file = tempfile.NamedTemporaryFile().name
        f = FilteredTextFile(os.path.join('sample', 'VersionInfoBean.java'))
        f.load()

        f.save(tmp_file)
        
        tf = FilteredTextFile(tmp_file)
        tf.load()
    
        self.assertEqual(f.contents, tf.contents)
        os.remove(tmp_file)

        tf.save()

        cf = FilteredTextFile(tmp_file)
        cf.load()
        self.assertEqual(f.contents, cf.contents)

    def test_accept_line(self):
        f = NoEmptyFilteredTextFile(os.path.join('sample', 'VersionInfoBean.java'))
        f.load()
        self.assertTrue(len(f.contents) > 0)

        for l in f.contents:
            self.assertTrue(len(l.strip()) > 0)

class FilteredJavaFileTest(unittest.TestCase):

    def test_init(self):
        f = FilteredJavaFile('file')
        self.assertEqual('file', f.file_name)
        self.assertEqual('utf-8', f.encoding)
        self.assertEqual([], f.contents)
        self.assertEqual(FilteredJavaFile.ST_START, f._state)

        f = FilteredJavaFile('file', 'iso-8859-1')
        self.assertEqual('file', f.file_name)
        self.assertEqual('iso-8859-1', f.encoding)
        self.assertEqual([], f.contents)
        self.assertEqual(FilteredJavaFile.ST_START, f._state)

    def test_load_no_license(self):
        f = FilteredJavaFile(os.path.join('sample', 'VersionInfoBean.java'))
        f.load()
        self.assertEqual('package it.is.just.a.test;', f.contents[0].strip())

    def test_load_with_license(self):
        f = FilteredJavaFile(os.path.join('sample', 'VersionInfoBeanLicensed.java'))
        f.load()
        self.assertEqual('package it.is.just.a.test;', f.contents[0].strip())

    def test_load_with_comment(self):
        f = FilteredJavaFile(os.path.join('sample', 'VersionInfoBeanWithComment.java'))
        f.load()
        self.assertEqual('// This should not be ignored', f.contents[0].strip())

    def test_load_with_comment2(self):
        f = FilteredJavaFile(os.path.join('sample', 'VersionInfoBeanWithComment2.java'))
        f.load()
        self.assertEqual('/* This should not be ignored */', f.contents[0].strip())

    def test_load_with_comment_and_license(self):
        f = FilteredJavaFile(os.path.join('sample', 'VersionInfoBeanWithCommentLicensed.java'))
        f.load()
        self.assertEqual('// This should not be ignored', f.contents[0].strip())

    def test_load_with_comment2_and_license(self):
        f = FilteredJavaFile(os.path.join('sample', 'VersionInfoBeanWithComment2Licensed.java'))
        f.load()
        self.assertEqual('/* This should not be ignored */', f.contents[0].strip())

    def test_load_with_comment3_and_license(self):
        f = FilteredJavaFile(os.path.join('sample', 'VersionInfoBeanWithComment3Licensed.java'))
        f.load()
        self.assertEqual('/* This should not be ignored */', f.contents[0].strip())

    def test_add_license(self):
        f = FilteredJavaFile(os.path.join('sample', 'VersionInfoBeanLicensed.java'))
        f.load()
        self.assertEqual('package it.is.just.a.test;', f.contents[0].strip())

        first_line = f.contents[0]
        license = ['this', 'is', 'it']
        f.add_license(license)
        for i in range(0, len(license)):
            self.assertEqual(license[i], f.contents[i])
        self.assertEqual(first_line, f.contents[3])

if __name__ == '__main__':
    unittest.main()

