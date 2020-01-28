#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 16:18:42 2019
@author: akshay72

Main file running the application.
"""

from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import db_config.dbManager as dbm
import logging
import psycopg2, config_parser

logging.basicConfig(level=logging.DEBUG)

start_time = ""
end_time = ""

server = Blueprint('server', __name__)


@server.route('/', methods=['GET', 'POST'])
def hello_world():
    return "<div><b>Sorry!!<br/>Only team has access to database<b><a href='/about'>About</a></div>"


@server.route('/about', methods=['GET', 'POST'])
def about():
    return jsonify({'Company': 'Visitor Management',
                    'Dev center': 'Team Foundation',
                    'version': 'heroku test development'})






































































