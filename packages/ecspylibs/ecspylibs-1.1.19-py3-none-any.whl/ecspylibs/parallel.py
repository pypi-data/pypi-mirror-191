#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Wed Feb 8 12:50:20 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

"""
blah
"""

import time
from autologging import logged, traced


@traced
@logged
class Parallel:
    """
    Blah
    """

    def __init__(self, process, pool_executor, pool_size=None):
        """
        Blah
        """

        self.run_time = None
        self.results = None
        self.arguments = None
        self.process = process
        self.pool_executor = pool_executor
        self.pool_size = pool_size

        if self.pool_size:
            if isinstance(self.pool_size, int) or self.pool_size.isnumeric():
                self.pool_size = int(self.pool_size)
            else:
                self.pool_size = None
        else:
            self.pool_size = None

        self.__log.debug(f"Process       : {type(self.process)}")
        self.__log.debug(f"Pool Executor : {self.pool_executor}")
        self.__log.debug(f"Pool Size     : {self.pool_size}")

    def run(self, arguments):
        """
        Blah
        """

        self.arguments = arguments

        self.__log.debug(f"arguments   : {self.arguments}")

        start_time = time.perf_counter()

        with self.pool_executor(self.pool_size) as executor:
            self.results = executor.map(self.process, self.arguments)

        finish_time = time.perf_counter()

        self.run_time = finish_time - start_time

        return self.results
