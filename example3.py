import pywese

def respond(request):
	print("responding..")
	try:
		f = open(request['FILENAME'], "r")
		buf = f.read()
		f.close()
		if request['FILENAME'] == "example3result.html":
			buf = buf % request['GET']
		return buf
	except:
		print("Unknown " + request['FILENAME']);
		return ""

print("Serving example2")
pywese.HttpServer("localhost", 8080, respond)
