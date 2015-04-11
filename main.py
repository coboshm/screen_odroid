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
from player import *
from scheduler import *
from associate_screen import *
from webcam import *
import os
from time import sleep
import threading


def player_bucle():
	scheduler2 = scheduler();
	if scheduler2.get_status() != 0:
		sleep(15)
		#here i have to open no internet connexion state
		player_bucle()
	else:
		cmd = ["chromium-browser", "--kiosk", "--user-data-dir", 'http://localhost:3000']
		proc1 = subprocess.Popen(cmd);
		while proc1.poll() is None:
			sleep(300)
			scheduler2 = scheduler();
		player_bucle()
		


def main(argv=None):
	config = configparser.ConfigParser();
	config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));

	url_assets = os.path.abspath(os.path.dirname(__file__))+'/playlist'
	url_templates = os.path.abspath(os.path.dirname(__file__))+'/templates'

	
	
	if config['DEFAULT']['active'] != '1':
		cmd = ["chromium-browser", "--kiosk", "--user-data-dir", 'http://localhost:3000']
		proc1 = subprocess.Popen(cmd);
		while config['DEFAULT']['active'] != '1' and config['DEFAULT']['code_screen'] == '':
			sleep(10)
			config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));
		while config['DEFAULT']['active'] != '1' and config['DEFAULT']['code_screen'] != '':
			active_screen(config['DEFAULT']['code_screen'])
			sleep(10)
			config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));

	

	t1 = threading.Thread(target=cameraDetection)
	t1.start()

	player_bucle()
	

	
	return

if __name__ == "__main__":
  sys.exit(main())
