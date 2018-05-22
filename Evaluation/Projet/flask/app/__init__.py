# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
# app.config['JSON_AS_ASCII'] = True
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
from app import views
