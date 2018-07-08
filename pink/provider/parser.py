#!/usr/bin/env python
# -*- coding: utf-8 -*-
from provider import Provider


class Parser:

    @staticmethod
    def get_provider(pink_def):
        for clazz in Provider.__subclasses__():
            obj = clazz.__new__(clazz)
            match = obj.match(pink_def)
            if match:
                return obj
