#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
# app.py:
#
# ------------------------------------------------------------------------------
#
# History:
#   2017-08-08 Initial version by Bernard Tsai (bernard@tsai.eu)
#
# ------------------------------------------------------------------------------

import os

from flask       import Flask, request, redirect
from yaml        import safe_dump
from json        import dumps
from yaml        import safe_load

from model.core.validate import Validate

app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# ------------------------------------------------------------------------------
#
# index: entry page
#
# ------------------------------------------------------------------------------
@app.route('/')
def index():
    #return app.send_static_file('html/index.html')
    return redirect("static/html/index.html", code=302)

# ------------------------------------------------------------------------------
#
# version: version of the application server
#
# ------------------------------------------------------------------------------
@app.route('/version')
def version():
    return "0.1.0"

# ------------------------------------------------------------------------------
#
# context: list of contexts
#
# ------------------------------------------------------------------------------
@app.route('/context' )
def listContexts():
    root_dir  = os.path.dirname(__file__)
    data_dir  = os.path.join( root_dir, "..", "..", "data", "models" )

    entries = os.listdir( data_dir )

    dirs = ""
    for entry in entries:
        path = os.path.join( data_dir, entry )
        if os.path.isdir( path ):
            dirs = dirs + "\n" + entry

    return dirs

# ------------------------------------------------------------------------------
#
# context/<context>: list of versions
#
# ------------------------------------------------------------------------------
@app.route('/context/<context>' )
def listVersions(context):
    root_dir  = os.path.dirname(__file__)
    data_dir  = os.path.join( root_dir, "..", "..", "data", "models", context )

    entries = os.listdir( data_dir )

    versions = ""
    for entry in entries:
        versions = versions + "\n" + entry[:-5]

    return versions

# ------------------------------------------------------------------------------
#
# context/<context>/<version>: get model
#
# ------------------------------------------------------------------------------
@app.route('/context/<context>/<version>' )
def getModel(context,version):
    root_dir  = os.path.dirname(__file__)
    file_name = os.path.join( root_dir, "..", "..", "data", "models", context, version + ".yaml" )

    with open( file_name, "r" ) as stream:
        model = stream.read()

    return model

# ------------------------------------------------------------------------------
#
# set: update VNF model
#
# ------------------------------------------------------------------------------
@app.route('/api/v0.1.0/set', methods=['POST'])
def set():
    descriptor = request.form['descriptor']

    # validate data schema
    # load vnf
    # apply change
    #   calculate new model
    #   calculate actions
    # save vnf & actions
    # render result

    validator = Validate()
    validator.version = "V0.0.1"

    data = safe_load( descriptor )
    messages = validator.validate( data )

    result = ""
    for msg in messages:
        result = result + str(msg) + "\n"

    return result

# ------------------------------------------------------------------------------
#
# main: run application server
#
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
