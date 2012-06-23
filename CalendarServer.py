import os
import pywese
import template

def serveImages(req):
	print('serveImages')
	global config
	try:
		contentType = pywese.getContentTypeByExt(req['FILENAME'].split('.')[-1])
		f = open(os.path.join(config['basePath'], req['FILENAME']), "r")
		buf = pywese.response(200, contentType, f.read())
		f.close()
	except:
		buf = pywese.response(404, contentType, "Image not found")
	return buf

def serveHtmlPages(req):
	print('serveHtmlPages')
	global config
	try:
		ext = req['FILENAME'].split('.')[-1]
		f = open(os.path.join(config['basePath'], req['FILENAME']), "r")
		buf = pywese.response(200, "text/"+ext, f.read())
		f.close()
	except:
		buf = pywese.response(404, "text/html", "Page not found")
	return buf

def servePyScripts(req):
	print('servePyScripts')
	global config
	try:
		# por o modulo template dentro do dict script
		oldPath = os.getcwd()
		os.chdir(os.path.dirname(os.path.join(config['basePath'], req['FILENAME'])))
		script = {}
		execfile(req['FILENAME'], script)
		script['template'] = __import__('template')
		buf = pywese.response(200, "text/html", script['run'](req))
		os.chdir(oldPath)
	except Exception, info:
		buf = pywese.response(404, "text/html", str(info))
	return buf

def serveDefault(req):
	req['FILENAME'] = 'index.py'
	return servePyScripts(req)

config = pywese.config("CalendarConfig")

server = pywese.HttpServer(
	config['host'],
	config["port"],
	[
		["^\w+\.(jpg|png|ico)$", serveImages],
		["^\w+\.(htm|html|css)$", serveHtmlPages],
		["^\w+\.py$", servePyScripts],
		["^$", serveDefault]
	],
	config['debug']
)
