#PyWeSe - Build web services

*PyWeSe - Python Web Server*

Pywese is an API to help build custom web server  

'Hello web' example:
	
	import pywese
	pywese.HttpServer("localhost", 8080, lambda request: "Hello web!!")


html server example:
	
	import pywese

	def page(request):
		try:
    		f = open(request['FILENAME'], "r")
			buf = pywese.response(200, f.read())
			f.close()
		except:
			buf = pywese.reponse(404, "Page '" + request['FILENAME'] + "' Not Found")
		return buf

	pywese.HttpServer("localhost", 8080, ["^.\*?.html$" : page])


