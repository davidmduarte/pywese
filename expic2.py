# this one does not work
import pywese

def imgs(req):
	f =open(req["FILENAME"], "r")
	buf = f.read()
	f.close()
	return buf

def pages(req):
	return "<h1>Serving Pages...</h1>"

pywese.HttpServer("localhost", 8080, {
	"*.jpg | *.png | *.gif | *.pdf" : imgs,
	"*"                             : pages
})
