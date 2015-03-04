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

def main(argv=None):
	config = configparser.ConfigParser();
	config.read('config.ini');
	
	scheduler2 = scheduler();
	asset = scheduler2.get_next_asset();
	
	file_name = asset["path"].split('/')[-1]
	playVideo_browser(file_name, config['DEFAULT']['url_assets'])
	
	return

if __name__ == "__main__":
  sys.exit(main())
