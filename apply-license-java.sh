#!/bin/bash
# apply-license-java.py - A simple tool to add license information to the beginning of java files
# Copyright (c) 2019, Fabio Jun Takada Chino. All rights reserved.
# This script is licensed under the termos of BSD 3-Clause License. 
# See https://github.com/fjtc/apply-license-java for further information

# Determine the current directory
CURR_DIR=$(pwd)

# Determine my home
MY_HOME=$(dirname $0)
pushd "$MY_HOME" > /dev/null
MY_HOME=$(pwd)
popd > /dev/null

APPLY_LICENSE_JAVA="$MY_HOME/apply-license-java.py"
PYTHON_BIN=python3

for f in `find $CURR_DIR -type f | grep .java$`; do
    "$PYTHON_BIN" "$APPLY_LICENSE_JAVA" "$f"
done
