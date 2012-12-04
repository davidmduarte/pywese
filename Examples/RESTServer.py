import pywese

sporting = {
	'team' : {
		'players' : [
			{
				'name' : "Rui Patricio",
				'position' : "Guarda Redes",
				'stats' : {
					'games' : 45,
					'defenses' : 99,
					'scored goals' : 0,
					'sufered goals' : 8,
					'passes' : 30
				}
			}
		],
		'coach' : 'Frank Vercauteren'
	},
	'president' : 'Godinho Lopes'
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
	global sporting
	return pywese.response(200, 'html/txt', str(sporting['team']))

def funcCoach(request):
	global sporting

	if request['REQUEST_METHOD'] == 'GET':
		return pywese.response(200, 'html/text', "Coach: " + sporting['coach'] + "<br>")
	elif request['REUQEST_METHOD'] == 'POST':
		sporting['coach'] = request['POST']['name']
		return pywese.response(201, 'html/text', "done<br>/sporting/team/Coach GET to see")
	elif request['REUQEST_METHOD'] == 'PUT':
		sporting['coach'] += request['POST']['name']
		return pywese.response(200, 'html/text', "done<br>/sporting/team/Coach GET to see")
	else:
		sporting['coach'] = None 
		return pywese.response(200, 'html/text', "done<br>/sporting/team/Coach GET to see")

pywese.HttpServer("localhost", 8080, {
	"^/sporting$": funcHelp,
	"^/sporting/team$": funcTeam,
	"^/sporting/team/coach$": funcCoach,
	"^/sporting/team/players$": funcPlayers,
	"^/sporting/team/players/(\d*)$": funcPlayers,
	"^/sporting/team/players/(\d*)/stats$": funcPlayersStats,
	"^/sporting/president$" : funcPresident
})
