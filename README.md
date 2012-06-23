PyWeSe - Build custom web servers

Examples:

#----begin-----
# Hello web exmple
import pywese
pywese.HttpServer("localhost", 8080, lambda request: "Hello web!!")
#----end-----

#----begin----
# html pages web server example
import pywese

def page(request):
	try:
    	f = open(request['FILENAME'], "r")
		buf = pywese.response(200, f.read())
		f.close()
	except:
		buf = pywese.reponse(404, "Page '" + request['FILENAME'] + "' Not Found")
	
	return buf

pywese.HttpServer("localhost", 8080, ["^.*?.html$" : page])
#----end----



