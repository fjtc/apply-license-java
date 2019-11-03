#!/usr/bin/python
# -*- coding: utf-8 -*-
# apply-license-java.py - A simple tool to add license information to the beginning of java files
# Copyright (c) 2019, Fabio Jun Takada Chino. All rights reserved.
# This script is licensed under the termos of BSD 3-Clause License. 
# See https://github.com/fjtc/apply-license-java for further information
import io
import os
import sys
from common import FilteredTextFile
from common import FilteredJavaFile

MY_HOME = os.path.dirname(os.path.realpath(__file__))
LICENSE_FILE = os.path.join(MY_HOME, 'license.txt')

# Check the parameters
if len(sys.argv) != 2:
    print('Usage: {} <java file>'.format(sys.argv[0]))
    sys.exit(1)
src_file = sys.argv[1]

# Check the license file
license_file = FilteredTextFile(LICENSE_FILE)
try:
    license_file.load()
except:
    print('License file {} could not be loaded.'.format(license_file.file_name))
    sys.exit(2)

# Load the java file
java_file = FilteredJavaFile(src_file)
try:
    java_file.load()
except:
    print('Java file {} could not be loaded.'.format(java_file.file_name))
    sys.exit(3)
if len(java_file.contents) == 0:
    print('The Java file {} is empty or broken.'.format(java_file.file_name))
    sys.exit(4)

# Save the backup file
try:
    java_file.save(java_file.file_name + '.bak')
except:
    print('Unable to create the backup for the file {}.'.format(java_file.file_name))
    sys.exit(5)

# Add the license and save the result
java_file.add_license(license_file.contents)
try:
    java_file.save()
except:
    print('Unable save the new version of the file {}.'.format(java_file.file_name))
    sys.exit(5)
