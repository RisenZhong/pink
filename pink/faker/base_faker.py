#!/usr/bin/env python
# -*- coding: utf-8 -*-

from faker import Faker


class BaseFaker:

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
