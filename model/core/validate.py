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
                messages.append( "Unknown type" )
            else:
                # load schema
                schema_name = data["type"]
                schema      = Validate.schemas[ schema_name ]

                # validate
                v = jsonschema.Draft4Validator( schema )
                for error in v.iter_errors(data):
                    messages.append( error.message )
        except Exception as e:
            messages.append( e.message )

        return messages
