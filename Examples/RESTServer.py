import pywese

sporting = {
	'team' : {
		'players' : [
			{
				'id' : 0,
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
		GET /sporting<br>
		GET /sporting/team<br> 
		GET|POST|PUT|DELETE /sporting/team/coach<br>
		GET|POST|DELETE /sporting/team/players<br>
		GET|PUT|DELETE /sporting/team/players/{id}<br>
		GET /sporting/team/players/{id}/stats<br>
		GET|POST|PUT|DELETE /sporting/president<br>
	""")

def funcTeam(resquest):
	global sporting
	return pywese.response(200, 'html/txt', str(sporting['team']))

def funcCoach(request):
	global sporting
	if request['REQUEST_METHOD'] == 'GET':
		return pywese.response(200, 'html/text', "Coach: " + sporting['team']['coach'] + "<br>")
	elif request['REQUEST_METHOD'] == 'POST':
		sporting['team']['coach'] = request['POST']['name']
		return pywese.response(201, 'html/text', "done<br>/sporting/team/Coach GET to see")
	elif request['REQUEST_METHOD'] == 'PUT':
		sporting['team']['coach'] += request['POST']['name']
		return pywese.response(200, 'html/text', "done<br>/sporting/team/Coach GET to see")
	else:
		sporting['team']['coach'] = None 
		return pywese.response(200, 'html/text', "done<br>/sporting/team/Coach GET to see")

def funcPlayers(request, playerId):
	global sporting
	if request['REQUEST_METHOD'] == 'GET':
		return pywese.response(200, 'json', "players: " + str(sporting['team']['players']))
	elif request['REQUEST_METHOD'] == 'POST':
		sporting['team']['players'].append({
			'id':  len(sporting['team']['players']) - 1
			'name': request['POST']['name'],
			'position': request['POST']['position'],
			'stats' : {}
		})
		return pywese.response(201, 'html/text', "done")
	elif request['REQUEST_METHOD'] == 'PUT':
		if playerId == None:
			return pywese.response(404, 'html/text', "Player Id needed")
		else:
			sporting['team']['players'][playerId]['nome'] = request['POST']['name']
			sporting['team']['players'][playerId]['position'] = request['POST']['name']
			return pywese.response(200, 'html/text', "")

		for player in sporting['team']['players']:
			if player['name'] == request['POST']['name']:
				player['position'] = request['POST']['position']
		return pywese.response(200, 'html/text', "done<br>/sporting/team/players GET to see")
	else:
		for player in sporting['team']['players']:
			if player['name'] == request['POST']['name']:
				sporting['team']['players'].remove(request['POST']['name'])
				break
		return pywese.response(200, 'html/text', "done<br>/sporting/team/Coach GET to see")

def funcPLayersStats(request, playerId):
	global sporting

pywese.HttpServer("localhost", 8080, {
	"^/sporting$": funcHelp,
	"^/sporting/team$": funcTeam,
	"^/sporting/team/coach$": funcCoach,
	"^/sporting/team/players$": funcPlayers,
	"^/sporting/team/players/(\d*)$": funcPlayers,
	"^/sporting/team/players/(\d*)/stats$": funcPlayersStats,
	"^/sporting/president$" : funcPresident
})
