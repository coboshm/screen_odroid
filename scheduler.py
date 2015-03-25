
"""
Simple module to download the files that we have to play and the schedul
"""
__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'

import configparser
import requests
import json
import urllib2
import shutil
import os

config = configparser.ConfigParser();
config.read('config.ini');

url_assets = os.path.abspath(os.path.join(os.path.dirname(__file__),'/playlist'))
url_assets_new = os.path.abspath(os.path.join(os.path.dirname(__file__),'/playlist_new'))
url_templates = os.path.abspath(os.path.join(os.path.dirname(__file__),'/templates'))

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
	u = urllib2.urlopen('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + row["path"]);

	file_name = row["path"].split('/')[-1]

	if not path.isdir(url_assets_new):
		makedirs(url_assets_new)
	if path.isfile(url_assets + '/' +file_name):
		os.rename(url_assets + '/' +file_name, url_assets_new + '/' +file_name)
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

	shutil.rmtree(url_assets)
	if not path.isdir(url_assets):
		makedirs(url_assets)
	shutil.move(url_assets, url_assets_new)
	shutil.rmtree(url_assets_new)



class scheduler(object):

	def __init__(self, *args, **kwargs):

		
		if internet_on(config['DEFAULT']['host'], config['DEFAULT']['port']):
			
			req = urllib2.Request('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + '/api/playlist')
			req.add_header('Content-Type', 'application/json');
			data = {'code': config['DEFAULT']['code_screen']};
			response = urllib2.urlopen(req, json.dumps(data));
			
			assets = json.loads(response.read());
			self.assets = [item for item in assets[0]];
			
			for row in self.assets:
				copy(row);

			self.index = 0
			self.internet = 1
			self.nassets = len(self.assets);
			
			return
		else:
			self.nassets = 0
			self.index = 0
			self.assets = None
			return


	def get_next_asset(self):
		if self.nassets == 0:
			return None
		idx = self.index
		self.index = (self.index + 1) % self.nassets
		return self.assets[idx]

