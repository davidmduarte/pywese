import pywese

def index(request):
	print("responding..")
	print(request)
	outVars = {
		"loop" : "\n".join(["<h2>Teste 123</h2>" for i in xrange(10)])
	}
	return """
	<html>
		<head>
		</head>
		<body>
			%(loop)s
		</body>
	</html>
	""" % outVars

print("Serving example")
pywese.HttpServer("localhost", 8080, index)
