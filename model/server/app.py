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
