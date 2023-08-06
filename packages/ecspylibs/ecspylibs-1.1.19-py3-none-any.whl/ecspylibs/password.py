#!/usr/bin/env python3
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

# Futuristic implementation of commands.  Must be first from/import
# command.

from __future__         import print_function

# Python Standard libraries.

import autologging
import base64
import logging
import pickle

from Crypto.Cipher      import AES
from autologging        import logged, traced
from os                 import urandom


@traced
@logged
class Password:
    """Add, Delete, or return User ID and Password information stored in an application PW file."""

    def __init__(self, passwd_file):
        """Set up the Password environment."""

        self.ids = None
        self.pw = None
        self.BLOCK_SIZE = 32
        self.PADDING = "{"

        self.passwd_file = passwd_file

        try:
            self.data = pickle.load(open(self.passwd_file, "rb"))
            self.secret = self.data["secret"]
            self.passwd = self.data["passwd"]
            self.__log.debug("Successfully read the password file '%s'.", self.passwd_file)
        except Exception as e:
            self.secret = urandom(self.BLOCK_SIZE)
            self.passwd = {}
            self.data = {"secret": self.secret, "passwd": self.passwd}
            self.__log.warning("Password file, '%s', is missing or empty.", self.passwd_file)
            self.__log.warning("Creating new password file '%s'.", self.passwd_file)
            self.__log.exception("Exception: '%s'", e)

        self.cipher = AES.new(self.secret)

    def pad(self, passwd):
        """Passwords must be a fixed length, so pad short passwords to the correct len."""

        return passwd + (self.BLOCK_SIZE - len(passwd) % self.BLOCK_SIZE) * self.PADDING

    def update(self):
        """Update the PW file."""

        self.data = {"secret": self.secret, "passwd": self.passwd}
        pickle.dump(self.data, open(self.passwd_file, "wb"))
        return True

    def set(self, id, passwd):
        """Add/Modify a User/PW entry in the PW file."""

        self.passwd[id] = base64.b64encode(self.cipher.encrypt(self.pad(passwd)))
        self.update()
        return True

    def get(self, id):
        """Verify and return, if exists, the PW for the given ID."""

        if id in self.passwd:
            self.pw = self.cipher.decrypt(base64.b64decode(self.passwd[id])).decode("utf-8").rstrip(self.PADDING)
        else:
            self.pw = ""

        return self.pw

    def delete(self, id):
        """Verify and delete a ID/PW entry in the PW file."""

        if id in self.passwd:
            self.__log.warning("Deleting User id '%s'.", id)
            del self.passwd[id]
            self.update()
        else:
            self.__log.warning("Id '%s' does not exists.", id)

        return True

    def list_ids(self):
        """Generate a list of User ID in the PW file."""

        print("%s\n" % ("ID",))
        self.ids = list(self.passwd)
        self.ids.sort()
        for self.id in self.ids:
            print("%-10s" % (self.id,))

        return True

    def list_pws(self):
        """Generate a list of User ID and Passwords in the PW file."""

        print("%-15s %s\n" % ("ID", "Password"))
        self.ids = list(self.passwd)
        self.ids.sort()
        for self.id in self.ids:
            self.pw = self.get(self.id)
            print("%-15s %s" % (self.id, self.pw))

        return True
