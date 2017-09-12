#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
# input.py:
#
# A mixin class to provide functionality for reading data.
#
# ------------------------------------------------------------------------------

import yaml
import os

# ------------------------------------------------------------------------------
#
# Class Input
#
# ------------------------------------------------------------------------------
class Input():

    # --------------------------------------------------------------------------
    def input(self, directory="", context="default", version=1):

        try:
            filename = os.path.join( directory, context, str(version) + ".yaml" )

            with open( filename, 'r' ) as stream:
                self.model = yaml.safe_load( stream )["model"]
        except IOError as exc:
            print( exc )
            pass
