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
		for key in d.keys():
			getattr(self, key)(d[key])
			
	def queryString(self, s):
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
		
		# parse
		self.buffer = self.buffer.split("\n\n")
		if(len(self.buffer) > 1):
			self.rawPost = self.buffer[1]
		self.buffer = self.buffer[0]
		
		print(self.buffer[0])
		
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
		#print(str(self))

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
			
def response(code, contentType, buf):
	codes = {
		200 : "OK",
		404 : "Not Found",
		301 : "Moved Permanently",
		302 : "Moved Temporarily",
		303 : "See Other",
		500 : "Server Error"
	}
	return "HTTP/1.0 " + str(code) + " " + codes[code] + "\r\nContent-Type: " + contentType + "\r\nContent-Length: " + str(len(buf)) + "\r\n\r\n" + buf

class HttpServer():
	def __init__(self, host, port, func):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(2)
		while True:
			print("Wait a connection")
			conn, addr = s.accept()
			if type(func) == types.FunctionType:
				thread.start_new_thread(self.simple, (conn, func,))
			elif type(func) == types.DictType:
				thread.start_new_thread(sel.complex, (conn, func,))
			else:
				pass
			
	def simple(self, conn, func):
		conn.send(func(Http(conn)))
		conn.close()
		
	def complex(self. conn, dicio):
		req = Http(conn)
		for k, v in func:
			patern = re.compile(k)
			if patern.match(req["FILENAME"] > 0:
				conn.send(v(req))
				conn.close()
				break
		