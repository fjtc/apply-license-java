#!/usr/bin/python
# -*- coding: utf-8 -*-
import io

class FilteredTextFile:

    def __init__(self, file_name, encoding = 'utf-8'):
        self._file_name = file_name
        self._encoding = encoding
        self._contents = []

    @property
    def contents(self):
        return self._contents
    
    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @property
    def encoding(self):
        return self._encoding
    
    @encoding.setter
    def set_encoding(self, encoding):
        self._encoding = encoding

    def filter_line(self, line):
        return line

    def append(self, line):
        self._contents.append(line)

    def start_load(self):
        pass

    def load(self, file_name = None):

        if file_name == None:
            file_name = self.file_name

        self.start_load()
        self._contents = []
        with io.open(file_name, mode ='r', encoding = self.encoding) as inp:
            for line in inp:
                line = self.filter_line(line)
                if line != None:
                    self.append(line)
    
    def save(self, file_name = None):
        if file_name == None:
            file_name = self.file_name

        with io.open(file_name, mode = 'w', encoding = self.encoding) as outp:
            for line in self.contents:
                outp.write(line)

class FilteredJavaFile(FilteredTextFile):
    ST_START = 0
    ST_INITIAL_COMMENT = 1
    ST_INSIDE_CODE = 2

    def __init__(self, file_name, encoding = 'utf-8'):
        super().__init__(file_name, encoding)
        self._state = FilteredJavaFile.ST_START

    def _is_package_declaration(self, line):
        return line.lstrip().startswith('package')

    def start_load(self):
         self._state = FilteredJavaFile.ST_START

    def is_multi_line_comment_start(self, line):
        line = line.strip()
        if line.find('*/') != -1:
            # The block starts and ends in the same line
            return False
        elif line.startswith('/**') or line.startswith('/*!'):
            # Doxygen block
            return False
        elif line.startswith('/*'):
            return True
        else:
            return False

    def filter_line(self, line):
        if self._state == FilteredJavaFile.ST_INSIDE_CODE:
            return line
        elif self._state == FilteredJavaFile.ST_START:
            if self.is_multi_line_comment_start(line):
                self._state = FilteredJavaFile.ST_INITIAL_COMMENT
                return None
            else:
                self._state = FilteredJavaFile.ST_INSIDE_CODE
                return line
        elif self._state == FilteredJavaFile.ST_INITIAL_COMMENT:
            idx = line.find('*/')
            if idx == -1:
                return None
            else:
                self._state = FilteredJavaFile.ST_INSIDE_CODE
                line = line[(idx + 2):]
                if len(line.strip()) == 0:
                    return None
                else:
                    return line
        else:
            raise Exception('Invalid internal state {}.'.format(self._state))

    def add_license(self, license):
        for i in range(0, len(license)):
            self.contents.insert(i, license[i])
