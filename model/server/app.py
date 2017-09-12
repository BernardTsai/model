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
from model.cli.validator import Validator

app = Flask(__name__, static_url_path='/static')

# ------------------------------------------------------------------------------
#
# index: entry page
#
# ------------------------------------------------------------------------------
@app.route('/static')
def index():
    return app.send_static_file('html/index.html')
    # return redirect("../../static/html/index.html", code=302)

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
    vnf  = request.form['vnf']
    data = request.form['data']

    # validate data schema
    # load vnf
    # apply change
    #   calculate new model
    #   calculate actions
    # save vnf & actions
    # render result

    validator = Validator()
    validator.validate( data )

    result = ""
    for msg in validator.messages:
        result = result + msg + "\n"

    return result

# ------------------------------------------------------------------------------
#
# main: run application server
#
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
