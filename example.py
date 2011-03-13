import pywese

def index(sock):
	return """
	<html>
		<head>
		</head>
		<body>
			<h1>Teste 1 2 3</h1>
		</body>
	</html>
	"""
pywese.HttpSever("localhost", 8080, index)
