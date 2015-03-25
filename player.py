#!/usr/bin/env python

"""
Simple module to play items of scheduler
"""
__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'

import sys
import webbrowser


def playVideo_browser(filename, url_file, url_add):
	#maybe i have to add the tipe of all files type="video/mp4"
	url = url_add +'/player.html';
	html = ("<html><head><style>video#bgvid {position: fixed; right: 0; bottom: 0;"
			"min-width: 100%; min-height: 100%; width: auto; height: auto; z-index: -100;" 
			"background-size: cover;} </style></head><body><video autoplay id='bgvid'>"
			"<source src='"+url_file +"/"+ filename+"'></video></body><script>"
			"var video1 = document.getElementById('bgvid'); video1.addEventListener('ended', videoEndHandler, false);"
			"function videoEndHandler(e) { window.close(); } </script> </html>");
	f = open(url, 'w');
	f.write(html);
	f.close();
	webbrowser.open_new('file://'+url);
	return

def playImage_browser_expand(filename, url_file, url_add, duration):
	url = url_add +'/expandImage.html';
	html = ("<html><head><style> html { "
			"background:url('"+url_file +"/"+ filename+"')"
			" center center no-repeat; background-size: 100% 100%; } </style></head>"
			"<body></body><script> setTimeout(closeBrowser, "+ str(duration)  +"); function closeBrowser(e) {"
			"window.close(); } </script> </html>");
	f = open(url, 'w');
	f.write(html);
	f.close();
	webbrowser.open_new('file://'+url);
	return

def playImage_browser_originalSize(filename, url_file, url_add, duration):
	url = url_add +'/originalImage.html';
	html = ("<html><head><style> html {background:url('"+url_file +"/"+ filename+"') "
			"center center no-repeat;} </style></head><body></body><script>"
			"setTimeout(closeBrowser, "+ str(duration) + " );function closeBrowser(e) {"
			"window.close(); } </script></html>");
	f = open(url, 'w');
	f.write(html);
	f.close();
	webbrowser.open_new('file://'+url);
	return

def black_screen(url_add):
	url = url_add +'/black.html';
	webbrowser.open_new('file://'+url);
	return
