#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Thu Feb 2 13:41:03 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

# Futuristic implementation of commands.  Must be first from/import
# command.

from __future__ import print_function

# Python Standard libraries.

import autologging
import logging
import psutil

from autologging import logged, traced


@traced
@logged
class ReapChildren:
    """Locate all children processes, if any, and kill them."""

    def __init__(self):
      self.procs = None
      self.alive = None
      self.gone = None

    """Nothing to setup."""

    def reap_children(self, timeout=3):
        """Locate all children processes, if any, and kill them."""

        def on_terminate(proc):
            """Log any process killed by reapChildren."""

            self.__log.warning("Process %s terminated with exit code %s.", proc, proc.returncode)

        self.procs = psutil.Process().children(recursive=True)

        for self.p in self.procs:
            self.__log.warning("Process %s survived drive.quit(); trying SIGTERM!", self.p)
            self.p.terminate()

        self.gone, self.alive = psutil.wait_procs(self.procs, timeout=timeout, callback=on_terminate)

        if not self.alive:
            for self.p in self.alive:
                self.__log.error("Process %s survived SIGTERM; trying SIGKILL!", self.p)
                self.p.kill()

            self.gone, self.alive = psutil.wait_procs(self.alive, timeout=timeout, callback=on_terminate)

            if not self.alive:
                for self.p in self.alive:
                    self.__log.critical("Process %s survived SIGKILL; giving up!", self.p)
