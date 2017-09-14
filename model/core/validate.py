#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
# validate.py:
#
# A mixin class to provide functionality for reading data.
#
# ------------------------------------------------------------------------------

import yaml
import glob
import os
import jsonschema
import traceback

# ------------------------------------------------------------------------------
#
# Class Validate
#
# ------------------------------------------------------------------------------
class Validate():

    # --------------------------------------------------------------------------
    schemas = {}

    # --------------------------------------------------------------------------
    def validate(self, data):
        messages = []

        try:
            if not Validate.schemas:
                # initialize class attributes
                root_dir =  os.path.dirname(__file__)

                # load schemas
                for schema_file in glob.glob( '{}/../../schemas/{}/*.yaml'.format( root_dir, self.version ) ):
                    schema = os.path.basename( schema_file )[:-5]
                    with open( schema_file, 'r' ) as stream:
                        Validate.schemas[schema] = yaml.safe_load( stream )

            # check type
            if not data["type"] in Validate.schemas:
                messages.append( "Unknown type: " + data["type"] )
            else:
                # load schema
                schema_name = data["type"]
                schema      = Validate.schemas[ schema_name ]

                # validate
                v = jsonschema.Draft4Validator( schema )
                for error in v.iter_errors(data):
                    path = ""
                    for entry in error.absolute_path:
                        if isinstance( entry, int ):
                            path = path + "[" + str(entry) + "]"
                        else:
                            path = path + "/" + str(entry)
                    print(error.absolute_path )
                    print( "-" + path + "-")
                    if path == "":
                        path="/"

                    messages.append( path  + " <br/>")
                    messages.append( error.message + " <br/>")
        except Exception as e:
            traceback.print_exc()
            messages.append( e )

        return messages
