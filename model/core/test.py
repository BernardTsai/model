#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODOS:
# - better comments and docs
#
# -  check seperators of links "-" maybe replace with = and exclude = from names
# - get_interface delivers None - how to resolve if a false network has been used in xref (=> better validation?)
#
# - apply cluster info update if nodes are added or removed

# ------------------------------------------------------------------------------
#
# test.py:
#
# ------------------------------------------------------------------------------

import os
import yaml

from model  import Model
from delta  import Delta
from action import Action

# determine directories
root_dir  = os.path.dirname(__file__)
data_dir  = os.path.join( root_dir, "..", "..", "data", "test" )
model_dir = os.path.join( root_dir, "..", "..", "data", "models" )

# create model and apply changes
model = Model( "test")

list = [ "ExternalNetwork.yaml", "ExternalComponent.yaml", "VNF.yaml", "Tenant.yaml", "InternalNetwork.yaml", "InternalComponent.yaml", "Node.yaml" ]

for item in list:
    filename = os.path.join( data_dir, item )
    with open( filename, 'r' ) as stream:
        data = yaml.safe_load( stream )
    model.set( data )
    txt = model.render( "canonical" )
    model.output( txt, model_dir )

# determine difference between two versions
model3 = Model( "test" )
model3.input( model_dir, "test", 3 )

model7 = Model( "test" )
model7.input( model_dir, "test", 7 )

delta = Delta( model3, model7 )

txt = delta.render("delta")
print( txt )

print( "--------------------" )

# derive action plan
action = Action( delta )
txt = action.render( "action")
print( txt)
