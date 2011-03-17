import pywese

def respond(request):
	print("responding..")
	try:
		f = open(request['FILENAME'], "r")
		buf = f.read()
		f.close()
		return buf
	except:
		print("Unknown " + request['FILENAME']);
		return ""

print("Serving example2")
pywese.HttpServer("localhost", 8080, respond)
