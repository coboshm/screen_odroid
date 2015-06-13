#!/usr/bin/env python

"""
Simple module to connect with the cloud and associate the screen
"""

__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'

import sys
import os
import configparser
import requests
import json
import urllib2
import subprocess

def active_screen(code):
    config = configparser.ConfigParser();
    config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));
    req = urllib2.Request('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + '/api/is_active_screen')
    req.add_header('Content-Type', 'application/json');
    data = {'code': code};
    response = urllib2.urlopen(req, json.dumps(data));
    active = json.loads(response.read());
    return active





