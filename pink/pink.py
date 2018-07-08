#!/usr/bin/env python
# -*- coding: utf-8 -*-


usage = """
Usage:
  pink <command> [options]

Commands:
  fill                        Fill database.
  api                         Generate api case files.
  doc                         Generate db doc files.
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  --isolated                  Run pip in an isolated mode, ignoring
                              environment variables and user configuration.
  -v, --verbose               Give more output. Option is additive, and can be
                              used up to 3 times.
  -V, --version               Show version and exit.
  -q, --quiet                 Give less output. Option is additive, and can be
                              used up to 3 times (corresponding to WARNING,
                              ERROR, and CRITICAL logging levels).
"""


if __name__ == '__main__':
    print(usage)