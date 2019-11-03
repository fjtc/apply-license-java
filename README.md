# apply-license-java.py
Copyright (c) 2019, Fabio Jun Takada Chino. All rights reserved.

## Description

**apply-license-java.py** is a very simple script intended to add license information
to Java source files. It replaces the first multi-line comment block of the file with the
the license text inside the file **license.txt**. If the source file doesn't have the first
multi-line block, it will be added to it.

Although first developed for **Java**, any source code that supports the 
**Java**/**C**/**C++**/**C#** multi-line comment syntax be used with this tool.

## Usage

Just execute:

```
$ python apply-license-java.py <java source file>
```

It will generate the new file and also a backup file with the same name of the source file
appended with the suffix **.bak**.

We also provide a bash script called **apply-license-java.sh** that will scan the current
directory recursively and apply this tool to all **.java** files found in the tree.

## Set your license

To set your license, just change the contents of the file **license.txt**. It is important
to notice that it must be a single multi-line comment because it will be added to the
beginning of the file as is, without any transformation.

Set the license to something that is not a single multi-line comment may lead to unpredictable
results, specially when this tool is executed more than once.

## Dependencies

This script requires Python 3 to run properly.

## Limitations

This version has the following limitations:

1. Only UTF-8 enconded files are supported;
1. Java syntax is not validated;
1. The first multi-line comment of the file will be replaced by the license, regardless of its contents;

## Licensing

This script is licensed under the terms of **BSD 3-Clause License**. More
information inside the file [LICENSE](LICENSE).
