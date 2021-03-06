#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from faker import Faker


class Provider:

    def produce(self, pink_def):
        pass

    def match(self, pink_def):
        pass


class FakerProvider(Provider):

    pattern = '[a-z]+'

    def __init__(self, locale=None, seed=None):
        if not locale:
            self.factory = Faker()
        else:
            try:
                self.factory = Faker(locale)
            except AttributeError:
                print('Specified locale is not supported, using en_US')
                self.factory = Faker()
        if seed:
            self.factory.seed(seed)

    def produce(self, pink_def):
        return getattr(self.factory, pink_def)

    def match(self, pink_def):
        match = re.fullmatch(self.pattern, pink_def)
        if match:
            return True
        return False


class ParentColumnProvider(Provider):
    pass


class EnumProvider(Provider):
    pass

