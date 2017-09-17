#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#  file:    validator.py
#  version: 1.0
#  date:    15.09.2017
#  author:  Bernard Tsai (bernard@tsai.eu)
#  description:
#    This script allows to validate change requests.
#
# ------------------------------------------------------------------------------
# TODO:
#  - better error handling
# ------------------------------------------------------------------------------

import os
import argparse
import yaml
import sys

from model.core.input    import Input
from model.core.validate import Validate

# ------------------------------------------------------------------------------
class Program():

    # --------------------------------------------------------------------------
    def __init__(self, change_file ):
        '''load entity from file or stdin'''

        # A) CONFIGURATION
        root_dir   = os.path.dirname(__file__)
        schema_dir = os.path.join( root_dir, "..", "..", "schemas" )

        # B) VALIDATION PHASE
        reader             = Input()
        data               = reader.read( change_file )

        validator          = Validate( directory=schema_dir )
        validation_results = validator.validate( data )

        if validation_results:
            for result in validation_results:
                print( "  " + result )
            sys.exit( -1 )

# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
def main():
    # setup command line parser
    parser = argparse.ArgumentParser(
        prog        = "validator.py",
        description = "Validate change",
    )
    parser.add_argument("-i", "--input", type=str, help="Name of change descriptor file (default: STDIN)")
    args = parser.parse_args()

    # execute program
    prog = Program( args.input )

# ----- MAIN -------------------------------------------------------------------

if __name__ == '__main__':
    main()
