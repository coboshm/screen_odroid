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
from associate_screen import *
import os
from time import sleep

def main(argv=None):
	config = configparser.ConfigParser();
	config.read('config.ini');

	url_assets = os.path.abspath(os.path.dirname(__file__))+'/playlist'
	url_templates = os.path.abspath(os.path.dirname(__file__))+'/templates'

	

	black_screen(url_templates);
	if config['DEFAULT']['active'] != '1':
		active_screen(config['DEFAULT']['code_screen'])
		config.read('config.ini');
		if config['DEFAULT']['active'] != '1':
			if (config['DEFAULT']['code_screen'] == '') :
				r = requests.post('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + '/api/new_screen');
				config.set('DEFAULT','code_screen',r.json());
				with open('config.ini', 'wb') as configfile:
					config.write(configfile);
				showCode_browser(config['DEFAULT']['code_screen'], url_templates);

			else :
				#Case that already have code but not associated to a user 
				#we only have to show the code in firefox
				showCode_browser(config['DEFAULT']['code_screen'], url_templates);
		    
			while config['DEFAULT']['active'] != '1':
				active_screen(config['DEFAULT']['code_screen'])
				sleep(30)
				config.read('config.ini');
    
	scheduler2 = scheduler();
	asset = scheduler2.get_next_asset();
	file_name = asset["path"].split('/')[-1];
	while True:
		#os.system('setterm -cursor off')
		if asset["tipo"].split('/')[-2] == 'image':
			playImage_browser_expand(file_name, url_assets, url_templates, asset["duration"]*1000)
			duration = asset["duration"];
			asset = scheduler2.get_next_asset();
			file_name = asset["path"].split('/')[-1];
			sleep(duration-1)
		else:
			playVideo_browser(file_name, url_assets, url_templates)
			duration = asset["duration"];
			asset = scheduler2.get_next_asset();
			file_name = asset["path"].split('/')[-1];
			if asset["tipo"].split('/')[-2] == 'image':
				sleep(duration-1)
			else:
				sleep(duration-0.5)

		
	return

if __name__ == "__main__":
  sys.exit(main())
