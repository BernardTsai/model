#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#  file:    comparator.py
#  version: 1.0
#  date:    15.09.2017
#  author:  Bernard Tsai (bernard@tsai.eu)
#  description:
#    This script allows to compare two models.
# ------------------------------------------------------------------------------
# TODO:
#  - better error handling
# ------------------------------------------------------------------------------

import os
import argparse
import yaml
import sys

from model.core.input    import Input
from model.core.model    import Model
from model.core.delta    import Delta
from model.core.render   import Render
from model.core.output   import Output

# ------------------------------------------------------------------------------
class Program():

    # --------------------------------------------------------------------------
    def __init__(self, input1_file, input2_file, template_file, output_file):
        '''Compare two models'''

        # A) CONFIGURATION
        root_dir   = os.path.dirname(__file__)
        tmpl_dir   = os.path.join( root_dir, "..", "..", "templates" )

        # B) INITIALIZATION PHASE
        reader = Input()

        data   = reader.read( input1_file )
        self.model1 = Model( model=data )

        data   = reader.read( input2_file )
        self.model2 = Model( model=data )

        # C) COMPARISON PHASE
        self.delta = Delta( self.model1, self.model2 )

        # D) RENDERING PHASE
        renderer = Render( directory=tmpl_dir )
        txt      = renderer.render( self.delta.getModel(), template_file )

        # E) TERMINATION PHASE
        writer = Output()
        writer.write2( output_file, txt )

# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
def main():
    # setup command line parser
    parser = argparse.ArgumentParser(
        prog        = "comparator.py",
        description = "Compare two models",
    )
    parser.add_argument("-i1", "--input1",                    type=str, help="Name of first model descriptor file")
    parser.add_argument("-i2", "--input2",                    type=str, help="Name of second model descriptor file")
    parser.add_argument("-t",  "--template", default="delta", type=str, help="Name of template (default: 'delta')")
    parser.add_argument("-o",  "--output",                    type=str, help="Name of output file (default: STDOUT)")
    args = parser.parse_args()

    # execute program
    prog = Program( args.input1, args.input2, args.template, args.output )

# ----- MAIN -------------------------------------------------------------------

if __name__ == '__main__':
    main()
