def index(get, post):
	return """
	<html>
		<head>
		</head>
		<body>
			<h1>Teste 1 2 3</h1>
		</body>
	</html>
	"""
server = HttpSever("localhost", 8080)
server.page("index.html", index)
server.listen()
