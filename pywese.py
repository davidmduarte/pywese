"HTTP Sever"
import sys
import os
import socket
import thread
import time

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

class HttpServer():
	def __init__(self, host, port, func):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(2)
		r = self.aux(func);
		r.next()
		while True:
			print("Wait a connection")
			conn, addr = s.accept()
			r.send(conn)

	def aux(self, func):
		while True:
			s = (yield)
			s.send(func(Http(s)))
			s.close()
def auxFunc(r,hash):
	for item in hash.keys:
