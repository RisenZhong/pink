#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Database:
    def __init__(self, name):
        self.name = name
        self.tables = []
        self.parent_columns = {}


class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns


class Column:
    def __init__(self):
        self.name = None
        self.type = None
        self.not_null = False
        self.faker_type = None
        self.parent_column = None
        self.values = []


class ParentColumn:
    def __init__(self):
        self.name = None
        self.values = []
        self.faker_type = None
