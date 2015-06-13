#!/usr/bin/env python
#!/usr/bin/env python
"""
Simple module to download the files that we have to play
"""
__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'

import sys
import subprocess
import configparser
from scheduler import *
from associate_screen import *
import os
from time import sleep

global active_iteration
active_iteration = 0

global opened_before_no_internet
opened_before_no_internet = 0

def internet_on(host, port):
    try:
        response=urllib2.urlopen('http://' + host + ':' + port ,timeout=20);
        return True
    except Exception as err: return False


def player_bucle():
	scheduler2 = scheduler();
	if scheduler2.get_status() != 0:
		cmd2 = ["chromium-browser", "--kiosk", "--user-data-dir", "--incognito", "--disable-cache",'http://localhost:3000/internet']
		sleep(35)
		#here i have to open no internet connexion state
		player_bucle_precharged(scheduler2)
	else:
		if active_iteration == 0:
			cmd = ["chromium-browser", "--kiosk", "--user-data-dir", "--incognito", "--disable-cache", 'http://localhost:3000']
			proc1 = subprocess.Popen(cmd);
		while True:
			sleep(20)
			scheduler2.refresh()
	return

def player_bucle_precharged(scheduler2):
	scheduler2.refresh();
	if scheduler2.get_status() != 0:
		cmd2 = ["chromium-browser", "--kiosk", "--user-data-dir", "--incognito", "--disable-cache",'http://localhost:3000/internet']
		sleep(35)
		#here i have to open no internet connexion state
		player_bucle_precharged(scheduler2)
	else:
		cmd = ["chromium-browser", "--kiosk", "--user-data-dir", "--incognito", "--disable-cache", 'http://localhost:3000']
		proc1 = subprocess.Popen(cmd);
		while True:
			sleep(20)
			scheduler2.refresh()
	return	

def activate_screen():
	config = configparser.ConfigParser();
	config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));
	if internet_on(config['DEFAULT']['host'], config['DEFAULT']['port']):
		if config['DEFAULT']['active'] != '1' and config['DEFAULT']['code_screen'] == '':
			active_iteration = 1
			cmd = ["chromium-browser", "--kiosk", "--user-data-dir", "--incognito",  "--disable-cache",'http://localhost:3000']
			proc1 = subprocess.Popen(cmd);
		else:
			if config['DEFAULT']['active'] != '1' and config['DEFAULT']['code_screen'] != '':
				x = active_screen(config['DEFAULT']['code_screen'])
				if x == 0:
					active_iteration = 1
					cmd = ["chromium-browser", "--kiosk", "--user-data-dir", "--incognito",  "--disable-cache",'http://localhost:3000']
					proc1 = subprocess.Popen(cmd);
				else:
					config.set('DEFAULT','active','1');
					with open(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')), 'wb') as configfile:
						config.write(configfile);
					try:
						player_bucle()
					except Exception as err: 
						player_bucle()

		while config['DEFAULT']['active'] != '1' and config['DEFAULT']['code_screen'] == '':
			sleep(10)
			config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));
		while config['DEFAULT']['active'] != '1' and config['DEFAULT']['code_screen'] != '':
			x = active_screen(config['DEFAULT']['code_screen'])
			if x == 1:
				config.set('DEFAULT','active','1');
				with open(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')), 'wb') as configfile:
					config.write(configfile);

				try:
					player_bucle()
				except Exception as err: 
					player_bucle()

			else:
				sleep(10)
				config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));
	else:
		if opened_before_no_internet == 0:
			cmd2 = ["chromium-browser", "--kiosk", "--user-data-dir", "--incognito", "--disable-cache",'http://localhost:3000/internet']
		sleep(35)
		opened_before_no_internet = 1
		activate_screen()

def main(argv=None):
	config = configparser.ConfigParser();
	config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));

	url_assets = os.path.abspath(os.path.dirname(__file__))+'/playlist'
	url_templates = os.path.abspath(os.path.dirname(__file__))+'/templates'

	if config['DEFAULT']['active'] != '1':
		activate_screen()
	else:
		player_bucle()
	
	return

if __name__ == "__main__":
  sys.exit(main())
