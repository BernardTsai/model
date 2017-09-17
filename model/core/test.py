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

from input    import Input
from validate import Validate
from model    import Model
from render   import Render
from output   import Output
from delta    import Delta
from action   import Action

# determine directories
root_dir   = os.path.dirname(__file__)
data_dir   = os.path.join( root_dir, "..", "..", "data", "test" )
model_dir  = os.path.join( root_dir, "..", "..", "data", "models" )
schema_dir = os.path.join( root_dir, "..", "..", "schemas" )
tmpl_dir   = os.path.join( root_dir, "..", "..", "templates" )

# create functions
reader    = Input( data_dir   )
validator = Validate( directory=schema_dir, version="V0.0.1" )
renderer  = Render( directory=tmpl_dir, version="V0.0.1" )
writer    = Output( model_dir )

print( renderer.getDirectory() )

# create model
model = Model( context="test", schema="V0.0.1" )

# apply changes one by one
list = [ "ExternalNetwork.yaml", "ExternalComponent.yaml", "VNF.yaml", "Tenant.yaml", "InternalNetwork.yaml", "InternalComponent.yaml", "Node.yaml" ]
for item in list:
    print( "----------" )
    print( item )

    # read change information
    data = reader.read( item )

    # validate change information
    validation_results = validator.validate( data )

    if validation_results:
        for result in validation_results:
            print( "  " + result )
        continue

    # apply change
    model.set( data )

    # render new version of the model
    obj = model.getModel()
    txt = renderer.render( obj, "canonical" )
    writer.write( txt )

# determine difference between two versions
reader2 = Input( model_dir + "/test" )

data3  = reader2.read( "3.yaml" )
model3 = Model( model=data3 )

data7  = reader2.read( "7.yaml" )
model7 = Model( model=data7 )

delta = Delta( model3, model7 )

txt = renderer.render( delta.model, "delta" )

print( "----------" )
print( txt )

# # derive action plan
action = Action( delta )
txt    = renderer.render( action.model, "action" )

print( "----------" )
print( txt )
