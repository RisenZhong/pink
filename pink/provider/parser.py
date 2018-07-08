#!/usr/bin/env python
# -*- coding: utf-8 -*-
from provider import Provider


class Parser:

    def get_provider(self, pink_def):
        subclasses__ = Provider.__subclasses__()
