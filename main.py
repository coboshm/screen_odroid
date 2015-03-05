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
from time import sleep

def main(argv=None):
	config = configparser.ConfigParser();
	config.read('config.ini');
	
	scheduler2 = scheduler();

	while True:
		asset = scheduler2.get_next_asset();
		file_name = asset["path"].split('/')[-1];
		if asset["tipo"].split('/')[-2] == 'image':
			playImage_browser_originalSize(file_name, config['DEFAULT']['url_assets'], config['DEFAULT']['url'], asset["duration"]*1000)
		else:
			playVideo_browser(file_name, config['DEFAULT']['url_assets'], config['DEFAULT']['url'])

		sleep(asset["duration"])
	return

if __name__ == "__main__":
  sys.exit(main())
