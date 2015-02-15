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

def showCode_browser(code, url_add):

    url = url_add + 'new_screen.html';
    html = ("<html><head><style>body {margin:50px 0px; padding:0px;text-align:center;} #Content "
            "{ width:500px; margin:0px auto; text-align:left; padding:15px; background-color:#eee; }"
            "</style></head><body><div id='Content'>"+code+"</div></body></html>");
    f = open(url, 'w');
    f.write(html);
    f.close();
    webbrowser.open_new('file://'+url);
    return

def main(argv=None):
    config = configparser.ConfigParser();
    config.read('config.ini');
    if (config['DEFAULT']['code_screen'] == '') :
        r = requests.post('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + '/api/new_screen');
        config.set('DEFAULT','code_screen',r.json());
        with open('config.ini', 'wb') as configfile:
            config.write(configfile);
        showCode_browser(config['DEFAULT']['code_screen'],config['DEFAULT']['url']);

    else :
        #Case that already have code but not associated to a user 
        #we only have to show the code in firefox
        showCode_browser(config['DEFAULT']['code_screen'],config['DEFAULT']['url']);
    
    return

if __name__ == "__main__":
  sys.exit(main())
