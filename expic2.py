# this one does not work
import pywese
import 

def imgs(req):
	f =open(req["FILENAME"], "r")
	buf = f.read()
	f.close()
	return buf

def pages(req):
	

pywese.HttpServer("localhost", 8080, {
	"^[a-zA-Z0-9\._]+?\.[gif|jpg|png|pdf]$" : imgs,
	"^[a-zA-Z0-9_]+$" : pages
})
