#!/usr/bin/env python

"""
Simple module to connect with the cloud and associate the screen
"""

__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'

import sys
import configparser
import requests
import webbrowser
import json
import urllib2

def showCode_browser(code, url_add):

    url = url_add +  '/new_screen.html';
    html = ("<html><head><style>body {margin:100px 0px; padding:0px;text-align:center; background: url('"+url_add+"/bg.jpg') no-repeat fixed center;" 
            " background-size: cover} #Content "
            "{ width:500px; margin:0px auto; text-align:left; padding:15px; margin-top:100px; background-color:#fff;"
            "-webkit-box-shadow: 4px 4px 0px 0px rgba(184,184,184,1); -moz-box-shadow: 4px 4px 0px 0px rgba(184,184,184,1);"
            "box-shadow: 4px 4px 0px 0px rgba(184,184,184,1); border-radius: 5px; }</style></head><body><img src='logo.png'/>"
            "<div id='Content'><span style='font-weight: bold; padding: 20px; font-family: Verdana, Geneva, sans-serif; '>Screen code:</span>"
            +code+"</div></body></html>");
    f = open(url, 'w');
    f.write(html);
    f.close();
    webbrowser.open_new('file://'+url);
    return


def active_screen(code):

    config = configparser.ConfigParser();
    config.read('config.ini');

    req = urllib2.Request('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + '/api/is_active_screen')
    req.add_header('Content-Type', 'application/json');
    data = {'code': code};
    response = urllib2.urlopen(req, json.dumps(data));

    active = json.loads(response.read());
    print active

    config.set('DEFAULT','active',str(active));
    with open('config.ini', 'wb') as configfile:
        config.write(configfile);
    return





