import pywese


def pages(req):
	if req['FILENAME'].split(".")[-1].upper() in ("JPG", "PNG"):
		f = open(req['FILENAME'], "r")
		buf = f.read()
		f.close()
		return buf
	else:
		return """
		<html>
		<body>
		A minha foto<br/>
		<img src="pic.jpg" border="1"><br/>
		clique <a href="pic.jpg">aqui</a> download(ar) a foto
		</body>
		</html>
		"""

pywese.HttpServer("192.168.2.100", 8080, pages)
#pywese.HttpServer("localhost", 8080, {
#	["*.jpg","*.png","*.gif"] : imgs,
#	"*"                       : pages
#})

