#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Wed Feb 1 18:00:52 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

"""
Doc String
"""

# Python Standard libraries.

import sys
from pathlib import Path
import logging
import os
import re
import time
from socket import gethostname
import autologging
import yaml
from autologging import logged, traced
from lxml import etree


@traced
@logged
class InitSetup:
    """Initialize the environment using command line parameters and init file."""

    def __init__(self, arguments: dict, default_arguments: dict, config=None, section=None):
        """Setup InitSetup"""

        self.arguments = arguments

        if config is not None:
            if config in self.arguments and self.arguments[config] is not None:
                config = self.arguments[config]
            elif config in default_arguments and default_arguments[config] is not None:
                config = default_arguments[config]
            else:
                config = False
        else:
            config = False

        if config:
            try:
                config = Path(config).resolve(strict=True)
            except FileNotFoundError as e:
                print(f"\n: Can't find configuration file {config=}\n", file=sys.stderr)
                print(f"\nFileNotFoundError: {e=}\n", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"\nException: {e=}\n", file=sys.stderr)
                sys.exit(2)

            with open(config, 'r') as file:
                config_yaml = yaml.safe_load(file)

            if 'config' not in config_yaml:
                print(f"\nError: Can't find dictionary 'config' in file '{config}'. Aborting!\n", file=sys.stderr)
                sys.exit(3)

            config_len = len(config_yaml['config'])
            section_number = 1

            if section and section in self.arguments and self.arguments[section]:
                if isinstance(self.arguments[section], int) or self.arguments[section].isnumeric():
                    section_number = int(self.arguments[section])
                else:
                    print(f"\nArgument section number '{section_number}' is missing or invalid", file=sys.stderr)
                    print(f"for file '{config}'.", file=sys.stderr)
                    print(f"Aborting!\n", file=sys.stderr)
                    sys.exit(4)

            elif 'section' in config_yaml:
                if isinstance(config_yaml['section'], int):
                    section_number = int(config_yaml['section'])

            if section_number > config_len or section_number <= 0:
                print(f"\nSection number '{section_number}' is out of range for file", file=sys.stderr)
                print(f"'{config}'.", file=sys.stderr)
                print(f"Aborting!\n", file=sys.stderr)
                sys.exit(5)

            self.data = config_yaml['config'][section_number - 1]

            for i in self.arguments:
                if self.arguments[i] is None:
                    if i[2:] in self.data:
                        self.arguments[i] = self.data[i[2:]]
                    elif i in default_arguments:
                        self.arguments[i] = default_arguments[i]
        else:
            for i in self.arguments:
                if self.arguments[i] is None:
                    if i in default_arguments:
                        self.arguments[i] = default_arguments[i]
