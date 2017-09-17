#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
# validate.py:
#
# A class to provide functionality for validating data.
#
# ------------------------------------------------------------------------------

import yaml
import glob
import os
import jsonschema

# ------------------------------------------------------------------------------
#
# Class Validate
#
# ------------------------------------------------------------------------------
class Validate():

    # --------------------------------------------------------------------------
    def __init__(self, version="V0.0.1", directory=None):
        """Initialize"""

        if directory is None:
            self.directory = os.path.dirname(__file__)
        else:
            self.directory = directory
        self.version    = version
        self.schemas    = {}
        self.validators = {}

        # load schemas
        for schema_file in glob.glob( '{}/{}/*.yaml'.format( self.directory, self.version ) ):
            schema_name = os.path.basename( schema_file )[:-5]
            with open( schema_file, 'r' ) as stream:
                schema    = yaml.safe_load( stream )
                validator = jsonschema.Draft4Validator( schema )

                self.schemas[schema_name]    = schema
                self.validators[schema_name] = validator

    # --------------------------------------------------------------------------
    def validate(self, data):
        """Validate data against a schema"""
        messages = []

        # check if type has been defined
        if not "type" in data:
            messages.append( "Missing type" )

        # check type
        elif not data["type"] in self.schemas:
            messages.append( "Unknown type: " + data["type"] )

        # validate against schema
        else:
            # load schema
            schema_name = data["type"]
            validator   = self.validators[ schema_name ]

            # validate
            for error in validator.iter_errors(data):
                path = ""
                for entry in error.absolute_path:
                    if isinstance( entry, int ):
                        path = path + "[" + str(entry) + "]"
                    else:
                        path = path + "/" + str(entry)
                if path == "":
                    path="/"

                messages.append( path  + ": " + error.message)

        return messages

    # --------------------------------------------------------------------------
    def getDirectory(self):
        """Provide directory"""
        return self.directory

    # --------------------------------------------------------------------------
    def getVersion(self):
        """Provide version"""
        return self.version

    # --------------------------------------------------------------------------
    def getSchemas(self):
        """Provide schemas"""
        return self.schemas
