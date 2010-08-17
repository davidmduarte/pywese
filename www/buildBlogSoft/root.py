def run(http):
	#import MySQLdb
	import sqlite3
	import template
	import time
	
	def sqliteDate2tuple(s):
		d = s.split(" ")
		d0 = map(int, d[0].split("-"))
		d1 = map(int, d[1].split(":"))
		return tuple(d0 + d1 + [0, 0, 0])
	
	def fetchall(cursor):
		a = []
		i = 0
		for row in cursor:
			d = {}
			for idx,col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			a.append(d)
			i += 1
		return a
	
	month = ['',
		u'January', u'February', u'March', u'April', u'May', u'June', u'July',
		u'August', u'September', u'October', u'November', u'December'
	]
	
	outp = {}
	#conn = MySQLdb.connect(host='localhost', user='root', passwd='4ay3rk3', db='buildblogsoft')
	conn = sqlite3.connect("buildBlogSoft.rsd")
	
	posts = conn.cursor()
	#posts = conn.cursor(MySQLdb.cursors.DictCursor)
	
	
	posts.execute("""
		SELECT id, titulo, artigo, estado, data_criacao, data_publicacao 
		FROM posts 
		WHERE estado = 1 ORDER BY data_publicacao DESC, id
	""")
	outp['posts'] = fetchall(posts)
	for i in xrange(len(outp['posts'])):
		outp['posts'][i]['dp'] = time.strftime("%A, %B %d, %Y", sqliteDate2tuple(outp['posts'][i]['data_publicacao']))
	
	#archive = conn.cursor(MySQLdb.cursors.DictCursor)
	archive = conn.cursor()
	archive.execute("""
		SELECT strftime('%Y', data_publicacao) as 'year', strftime('%m', data_publicacao) as 'month', count(*) as 'count'
		FROM posts
		GROUP BY strftime('%Y', data_publicacao), strftime('%m', data_publicacao)
		ORDER BY strftime('%Y', data_publicacao) DESC, strftime('%m', data_publicacao) DESC
	""")
	outp['archive'] = fetchall(archive)
	for i in xrange(len(outp['archive'])):
		outp['archive'][i]['month'] = month[int(outp['archive'][i]['month'])]
	
	if http['GET'].has_key('admin'):
		outp['logado'] = "Aqui vai a cena de admin caso esteja logado<br/>"
	
	archive.close()
	posts.close()
	conn.close()
	
	tmpl = template.Template("root.tmpl", outp)
	tmpl.parse()
	
	return tmpl.output()
