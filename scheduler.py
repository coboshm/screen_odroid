#!/usr/bin/env python
"""
Simple module to download the files that we have to play and the schedul
"""
__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'

import configparser
import subprocess
import requests
import json
import urllib2
import shutil
from time import sleep
from os import makedirs, path, rename
import uuid

url_assets = path.abspath(path.dirname(__file__))+'/playlist'
url_assets_new = path.abspath(path.dirname(__file__))+'/playlist_new'
url_templates = path.abspath(path.dirname(__file__))+'/templates'


def delete_folder(pth) :
    for sub in pth.iterdir() :
        if sub.is_dir() :
            delete_folder(sub)
        else :
            sub.unlink()
    pth.rmdir()

def internet_on(host, port):
    try:
        response=urllib2.urlopen('http://' + host + ':' + port ,timeout=20);
        return True
    except Exception as err: return False

def copy(row):
	config = configparser.ConfigParser();
	config.read(path.abspath(path.join(path.dirname(__file__),'config.ini')));
	u = urllib2.urlopen('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + row["path"]);

	file_name = row["path"].split('/')[-1]

	if not path.isdir(url_assets_new):
		makedirs(url_assets_new)
	if path.isfile(url_assets + '/' +file_name):
		rename(url_assets + '/' +file_name, url_assets_new + '/' +file_name)
	else:
		f = open(url_assets_new + '/' + file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (file_name, file_size)

		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break

			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status,

		f.close()
	



class scheduler(object):

	def __init__(self, *args, **kwargs):

		config = configparser.ConfigParser();
		config.read(path.abspath(path.join(path.dirname(__file__),'config.ini')));
		
		if internet_on(config['DEFAULT']['host'], config['DEFAULT']['port']):
			try:
				cmd = ["chromium-browser", "--kiosk", "--user-data-dir", "--incognito", "--disable-cache",'http://localhost:3000/downloading']
				browsr = subprocess.Popen(cmd);
				sleep(10)
				req = urllib2.Request('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + '/api/playlist')
				req.add_header('Content-Type', 'application/json');
				mac = "%12x" % uuid.getnode()
				data = {'code': config['DEFAULT']['code_screen'], 'mac': mac};
				response = urllib2.urlopen(req, json.dumps(data));
				
				assets = json.loads(response.read());
				with open(path.abspath(path.join(path.dirname(__file__),'playerlist.json')), 'w') as outfile:
					json.dump(assets, outfile)

				
				self.assets = [item for item in assets[0]];
				
				for row in self.assets:
					copy(row);

				if path.isdir(url_assets):
					shutil.rmtree(url_assets)
				if not path.isdir(url_assets):
					shutil.copytree(url_assets_new , url_assets)
				if path.isdir(url_assets_new):
					shutil.rmtree(url_assets_new)

				#self.index = 0
				#self.internet = 1
				#self.nassets = len(self.assets);

				self.status = 0
				#subprocess.Popen.kill(browsr)
				return
			except Exception as err:
				fname = path.abspath(path.join(path.dirname(__file__),'playerlist.json'))
				if path.isfile(fname):
					with open(path.abspath(path.join(path.dirname(__file__), '../.impactScreen/playerlist.json'))) as data_file:
						data = json.loads(data_file.read())
						self.assets = [item for item in data[0]];
						for row in self.assets:
							if not path.isfile(path.abspath(path.join(path.dirname(__file__), '../.impactScreen/playlist/'+str(row["path"].split('/')[-1])))):
								self.status = -1
								return

					self.status = 0
					return
				else:
					self.status = -1
					return
		else:
			fname = path.abspath(path.join(path.dirname(__file__),'playerlist.json'))
			if path.isfile(fname):
				with open(path.abspath(path.join(path.dirname(__file__), '../.impactScreen/playerlist.json'))) as data_file:
					data = json.loads(data_file.read())
					self.assets = [item for item in data[0]];
					for row in self.assets:
						if not path.isfile(path.abspath(path.join(path.dirname(__file__), '../.impactScreen/playlist/'+str(row["path"].split('/')[-1])))):
							self.status = -1
							return
				
				self.status = 0
				return
			else:
				self.status = -1
				return


	def get_status(self):
		#if self.nassets == 0:
		#	return None
		#idx = self.index
		#self.index = (self.index + 1) % self.nassets
		#return self.assets[idx]
		return self.status

	def refresh(self):
		return

