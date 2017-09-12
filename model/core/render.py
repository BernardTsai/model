#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
# render.py:
#
# A mixin class to provide functionality for rendering templates.
#
# ------------------------------------------------------------------------------

import os
import jinja2
import yaml

# ------------------------------------------------------------------------------
#
# Class Render
#
# ------------------------------------------------------------------------------
class Render():

    # --------------------------------------------------------------------------
    def render(self,template_name=None):

        # simply dump internal model if a template has not been provided
        if template_name is None:
            noalias_dumper = yaml.dumper.SafeDumper
            noalias_dumper.ignore_aliases = lambda self, data: True

            txt = yaml.dump(self.model, default_flow_style=False, Dumper=noalias_dumper)

            return txt

        # render model with template
        root_dir =  os.path.dirname(__file__)

        # load template
        template_file = '{}/../../templates/{}.j2'.format( root_dir, template_name )
        with open( template_file, 'r' ) as stream:
            template = stream.read()

        # initialize the jinja2 environment
        env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=[ 'jinja2.ext.loopcontrols' ]
        )

        # create template renderer
        renderer = env.from_string(template)

        # render the data
        txt = renderer.render(self.model)

        # return the results
        return txt
