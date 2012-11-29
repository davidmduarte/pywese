import os
import pywese

def serveImages(req):
	global config
	try:
		f = open(os.path.join(config['basePath'], req['FILENAME']), "r")
		buf = pywese.response(200, req['Content-Type'], f.read())
		f.close()
	except:
		buf = pywese.response(404, req['Content-Type'], "Image not found")
	return buf

def serveHtmlPages(req):
	global config
	try:
		f = open(os.path.join(config['basePath'], req['FILENAME']), "r")
		buf = pywese.response(200, "text/html", f.read())
		f.close()
	except:
		buf = pywese.response(404, req['Content-Type'], "Page not found")
	return buf

def servePyScripts(req):
	global config
	try:
		script = reload(os.path.join(config['basePath'], req['FILENAME']))
		buf = pywese.response(200, req['Content-Type'], script.run(req))
	except:
		buf = pywese.response(404, req['Content-Type'], "Script not found")
	return buf

config = pywese.config("config")

server = pywese.HttpServer(
	config['host'],
	config["port"],
	{
		"^[\w\/]+?\.gif|jpg|png$": serveImages,
		"^[\w\/]+?\.htm|html$": serveHtmlPages,
		"^[\w\/]+?\.py$": servePyScripts
	},
	config['debug']
)
