import pywese

def index(request):
	print("responding..")
	print(request)
	return """
	<html>
		<head>
		</head>
		<body>
			<h1>Teste 1 2 3</h1>
		</body>
	</html>
	"""

print("Serving example")
pywese.HttpServer("localhost", 8080, index)
