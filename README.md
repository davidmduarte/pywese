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

	pywese.HttpServer("localhost", 8080, {"^.\*?.html$" : page})


RESTfull server example:

	import pywese

	sporting = {
		'team' : 
		'coach' : None
	}

	def funcHelp(request):
		return pywese.response(200, 'html/txt', """
			/sporting GET<br>
			/sporting/team GET<br> 
			/sporting/team/coach GET, POST, PUT, DELETE<br>
			/sporting/team/players GET, POST, DELETE<br>
			/sporting/team/players/(\d*) GET, PUT, DELETE<br>
			/sporting/team/players/(\d*)/stats GET<br>
			/sporting/president GET, POST, PUT, DELETE<br>
		""")

	def funcTeam(resquest):
		return pywese.response(200, 'html/txt', """
			/sporting/team GET<br> 
			/sporting/team/coach GET, POST, PUT, DELETE<br>
			/sporting/team/players GET, POST, DELETE<br>
			/sporting/team/players/(\d*) GET, PUT, DELETE<br>
			/sporting/team/players/(\d*)/stats GET<br>
		""")

	def funcCoach(request):
		global sporting
		if request['REUQEST_METHOD'] == 'GET':
			return pywese.response(200, 'html/text', "Coach: " + sporting['coach'] + "<br>")
		elif request['REUQEST_METHOD'] == 'POST' or :
			sporting['coach'] = request['POST']['name']
			return pywese.response(201, 'html/text', "done<br>/sporting/team/Coach GET to see")
		elif request['REUQEST_METHOD'] == 'PUT':
			sporting['coach'] += request['POST']['name']
			return pywese.response(200, 'html/text', "done<br>/sporting/team/Coach GET to see")
		else:
			sporting['coach'] = None 
			return pywese.response(200, 'html/text', "done<br>/sporting/team/Coach GET to see")

	pywese.HttpServer("localhost", 8080, {
		"^/sporting$" : funcHelp,
		"^/sporting/team$" funcTeam: ,
		"^/sporting/team/coach$" : funcCoach,
		"^/sporting/team/players$" : funcPlayers,
		"^/sporting/team/players/(\d*)$" : funcPlayers,
		"^/sporting/team/players/(\d*)/stats$" : funcPlayersStats,
		"^/sporting/president$" : funcPresident
	})