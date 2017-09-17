#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#  file:    modeller.py
#  version: 1.0
#  date:   15.09.2017
#  author:  Bernard Tsai (bernard@tsai.eu)
#  description:
#    This script allows to create and update models and
#    render the results with the help of templates.
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
from model.core.model    import Model
from model.core.render   import Render
from model.core.output   import Output

# ------------------------------------------------------------------------------
class Program():

    # --------------------------------------------------------------------------
    def __init__(self, new_name, input_file, change_file, template_file, output_file):
        '''load entity from file or stdin'''

        # A) CONFIGURATION
        root_dir   = os.path.dirname(__file__)
        schema_dir = os.path.join( root_dir, "..", "..", "schemas" )
        tmpl_dir   = os.path.join( root_dir, "..", "..", "templates" )

        # B) INITIALIZATION PHASE

        # create a new model
        if new_name:
            self.model = Model( context=new_name )

        # load model (from STDIN or a file )
        else:
            # read change information
            reader = Input()
            data   = reader.read( input_file )

            self.model = Model( model=data )

        # C) MODIFICATION PHASE
        if change_file:
            reader             = Input()
            data               = reader.read( change_file )
            validator          = Validate( directory=schema_dir )
            validation_results = validator.validate( data )

            if validation_results:
                for result in validation_results:
                    print( "  " + result )
                sys.exit( -1 )

            self.model.set( data )

        # D) RENDERING PHASE
        renderer = Render( directory=tmpl_dir )
        txt      = renderer.render( self.model.getModel(), template_file )

        # E) TERMINATION PHASE
        writer = Output()
        writer.write2( output_file, txt )

# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
def main():
    # setup command line parser
    parser = argparse.ArgumentParser(
        prog        = "modeller.py",
        description = "Create / modify a VNF model",
    )
    parser.add_argument("-n", "--new",                           type=str, help="Name of new model descriptor (default: none)")
    parser.add_argument("-i", "--input",                         type=str, help="Name of input model descriptor file (default: STDIN)")
    parser.add_argument("-c", "--change",                        type=str, help="Name of change descriptor file (default: none)")
    parser.add_argument("-t", "--template", default="canonical", type=str, help="Name of template (default: 'canonical')")
    parser.add_argument("-o", "--output",                        type=str, help="Name of output model descriptor file (default: STDOUT)")
    args = parser.parse_args()

    # execute program
    prog = Program( args.new, args.input, args.change, args.template, args.output )

# ----- MAIN -------------------------------------------------------------------

if __name__ == '__main__':
    main()
