#!/usr/bin/env python

"""
Simple module to download the files that we have to play
"""
__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'

import sys
import configparser
from player import *
from scheduler import *
import os
from time import sleep

def main(argv=None):
	config = configparser.ConfigParser();
	config.read('config.ini');

	url_assets = os.path.abspath(os.path.dirname(__file__))+'/playlist'
	url_templates = os.path.abspath(os.path.dirname(__file__))+'/templates'

	scheduler2 = scheduler();

	black_screen(config['DEFAULT']['url']);

	while True:
		asset = scheduler2.get_next_asset();
		file_name = asset["path"].split('/')[-1];
		if asset["tipo"].split('/')[-2] == 'image':
			playImage_browser_originalSize(file_name, url_assets, url_templates, asset["duration"]*1000)
		else:
			playVideo_browser(file_name, url_assets, url_templates)

		sleep(asset["duration"]-1)
	return

if __name__ == "__main__":
  sys.exit(main())
