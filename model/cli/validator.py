#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#  file:    generator.py
#  version: 1.1
#  date:   25.01.2017
#  author:  Bernard Tsai (bernard@tsai.eu)
#  description:
#    This script loads a VNF descriptor
#    (special Tosca Simple Profile Format),
#    creates an internal intermediate model
#    and renders jinja2 templates
#    which it then returns as output.
# ------------------------------------------------------------------------------
#
# Requirements:
#   - PyYAML (3.12)
#   - Jinja2 (2.9.4)
#   - tosca-parser (0.7.0) (optional with DTAG extensions )
#
# ------------------------------------------------------------------------------
# TODO:
#  - routing information for components
# ------------------------------------------------------------------------------

import argparse
import yaml
import sys

from model.core.validate import Validate

# ------------------------------------------------------------------------------
class Validator(Validate):

    # --------------------------------------------------------------------------
    def __init__(self, filename=None):
        '''load entity from file or stdin'''

        # internal model
        self.model   = None
        self.version = "V0.0.1"

        # read from file or stdin and parse yaml to model
        if filename is not None:
            with open(filename, 'r') as stream:
                self.model = yaml.safe_load(stream)
        else:
            txt = ''
            for line in sys.stdin:
                txt += line

            self.model = yaml.safe_load(txt)

        # validate model
        self.messages = self.validate( self.model )

# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
def main():
    # setup command line parser
    parser = argparse.ArgumentParser(
        prog='validator.py',
        description='Validate entity',
    )
    parser.add_argument('-i', '--input', type=str, help='Input file (default: stdin)')
    args = parser.parse_args()

    # validate input
    validator = Validator( args.input )

    # check messages
    if validator.messages:
        index = 1
        for message in validator.messages:
            print( "{:>4}: {}".format(index, message) )
            index = index +1
        sys.exit(1)

# ----- MAIN -------------------------------------------------------------------

if __name__ == '__main__':
    main()
