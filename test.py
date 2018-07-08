#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

pattern = '\((.+)\)'

if __name__ == '__main__':
    s = 'kk(pyint[])'
    search = re.search(pattern, s)
    if search:
        print(search.group(1))