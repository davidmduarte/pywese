"HTTP Sever"
import sys
import os
import socket
import thread
import time
import types
import re

class Properties(dict):
	def __init__(self, **d):
		#print("Properties.__init__")
		for key in d.keys():
			getattr(self, key)(d[key])

	def queryString(self, s):
		#print("Properties.queryString")
		for item in s.split("&"):
			part = item.split("=")
			if len(part) == 1: self.__setitem__(part[0].replace("+", " "), '')
			else: self.__setitem__(part[0].replace("+", " "), part[1].replace("+", " "))

class Http(dict):
	def __init__(self, sock):
		self.buffer = ""
		self.rawPost = ""
		buf = sock.recv(512)

		while len(buf) == 512:
			self.buffer += buf
			buf = sock.recv(512)
		self.buffer += buf

		if len(self.buffer) > 0:
			# parse
			self.buffer = self.buffer.split("\n\n")
			if(len(self.buffer) > 1):
				self.rawPost = self.buffer[1]
			self.buffer = self.buffer[0]

			arr = self.buffer.split("\n")
			aux = arr.pop(0).split(' ')
			self.__setitem__('REQUEST_METHOD', aux[0])
			self.__setitem__('URI_STRING', aux[1])
			self.__setitem__('SERVER_PROTOCOL', aux[2])
			for line in arr:
				aux = line.split(':')
				if len(aux) > 1:
					self.__setitem__(aux[0], aux[1])
			aux = self.__getitem__('URI_STRING').split('?')
			if len(aux) == 0:
				self.__setitem__('FILENAME', 'root')
			else:
				self.__setitem__('FILENAME', aux[0][1:])
				if len(aux) > 1:
					self.__setitem__('GET', Properties(queryString = aux[1]))
				else:
					self.__setitem__('GET', {})
			self.__setitem__('POST', {})
			if self.has_key('Content-Length'):
				self.__setitem__('POST', Properties(queryString = self.rawPost))

	def getHeaders(self):
		return self.buffer

	def get(self):
		if self.has_key('GET'):
			print("-- GET: " + str(self.__getitem__('GET')))
			return self.__getitem__('GET')
		else:
			return {}

	def post(self):
		if self.has_key('POST'):
			print("-- POST: " + str(self.__getitem__('POST')))
			return self.__getitem__('POST')
		else:
			return {}

	def requestParams(self):
		ret = {}
		if self.has_key('POST'):
			ret = dict(ret.items() + self.__getitem__('POST').items())
		if self.has_key('GET'):
			ret = dict(ret.item() + self.__getitem__('GET').items())
		return ret

def responseWithCookies(code, contentType, cookies, buf):
	codes = {
		200 : "OK",
		201 : 'Created',
		404 : "Not Found",
		301 : "Moved Permanently",
		302 : "Moved Temporarily",
		303 : "See Other",
		500 : "Server Error"
	}

	if cookies == None:
		cookies = ""
	else:
		cookies = "Set-Cookie: ".join([";".join([key + "=" + cookie[key] for key in cookie.get_keys()]) for cookie in cookies])

	return "HTTP/1.0 " + str(code) + " " + codes[code] + "\r\nContent-Type: " + contentType + "\r\n" + cookies + "Content-Length: " + str(len(buf)) + "\r\n\r\n" + buf

def response(code, contentType, body, headers=None):
	codes = {
		200 : "OK",
		201 : "Created",
		404 : "Not Found",
		301 : "Moved Permanently",
		302 : "Moved Temporarily",
		303 : "See Other",
		500 : "Server Error"
	}

	
	return "HTTP/1.0 {code} {code_description}\r\nContent-Type: {content_type}\r\n{headers}\r\nContent-Lenght: {body_length}\r\n\r\n{body}".format(
		code = code,
		code_description = codes[code],
		content_type = contentType,
		headers = headers,
		body_length = len(body),
		body = body
	)
	

class HttpServer:
	def __init__(self, host, port, func, debug=False):
		self.host = host
		self.port = port
		self.debug = debug

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(10)
		while True:
			print("Wait a connection")
			conn, addr = s.accept()
			print("Request made")
			if type(func) == types.FunctionType:
				thread.start_new_thread(simpleParse, (conn, func,))
			elif type(func) == types.DictType:
				print("Dict Type")
				thread.start_new_thread(dictParse, (conn, func,))
			else:
				conn.send(response(404, "text/html", "Bad formed HTTPServer."))
				print('Bad formed HTTPServer.')

def simpleParse(conn, func):
	try:
		conn.send(func(Http(conn)))
		conn.close()
	except:
		conn.send(response(404, "text/html", "Http server could not responde"))
		print("Http server could not responde")

def dictParse(conn, obj):
	req = Http(conn)
	if req.has_key('URI_STRING'):
		for key in obj.keys():
			patern = re.compile(key)
			if patern.match(req['URI_STRING']) > 0:
				conn.send(obj[key](req))
				conn.close()
				break
		else:
			conn.send(response(404,'text/html', '404 File Not Found (get a better template)'))

def config(confFile):
	f = open(confFile, "r")
	d = eval(f.read())
	f.close()
	return d

def getContentTypeByExt(ext):
	hash = {
		'jpg'  : 'image/jpg',
		'png'  : 'image/png',
		'gif'  : 'image/gif',
		'html' : 'text/html',
		'txt'  : 'text/txt',
		'css'  : 'text/css'
	}

	if hash.has_key(ext):
		return hash[ext]
	else:
		return 'text/html'
