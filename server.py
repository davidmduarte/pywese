"HTTP Sever"
import sys
import os
import socket
import thread

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
			if len(aux[0]) == 0 or aux[0] == "/": self.__setitem__('FILENAME', 'root')
			else: self.__setitem__('FILENAME', aux[0][1:])
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

class Config(dict):
	def __init__(self):
		"""Esta class te que ler as configuracoes de um ficheiro mas por enquanto esta aqui predefinido"""
		f = file("config", "r")
		buf = f.read()
		for line in buf.split("\n"):
			aux = line.split("\t")
			self.__setitem__(aux[0], eval(aux[1]))
		f.close()
		
		self.__setitem__("BASEPATH", os.getcwd() + self.__getitem__('BASEPATH'))
		sys.path.append(self.__getitem__('BASEPATH'))
		os.chdir(self.__getitem__('BASEPATH'))
		
		
#def debug(http):
#	if http['__DEBUG__'] == True:
#		while True:
#			f = open(http['FILENAME'], "r")
#			buf = f.read()
#			i=1
#			for l in buf.split("\n"):
#				print(str(i) + " => " + l)
#			f.close()
#			o = raw_input("=> ")
		
def respond(s):
	print("Responding..")
	http = Http(s)
	print(http)
	if http['Accept'].find("text") == -1:
		f = open(config['BASEPATH'] + "/" + http['FILENAME'], "rb")
		s.send(f.read())
		f.close()
	else: 
		m = None
		try:
			m = __import__(http['FILENAME'])
			m = reload(m)
			s.send(m.run(http))
		except ImportError:
			s.send("<html><body><h1>PAgE nOt fOUnd</h1></body></html>")
		except Exception, err:
			s.send("<html><body><b>ERROR:</b> " + str(err) + "</body></html>")
		#buffer = "<br>".join(http.getHeaders().split("\n")) + m.run(http) 
		#s.send(buffer)
		#if(config['DEBUG'] == True):
		#	thread.start_new_thread( debug, (http,))
	s.close()
	print("Responded")

if __name__ == '__main__':
	print("Start Server.py")
	print("Loading configurations ...")
	config = Config()
	print("Initializing Socket (Listening at port %d) ..." % (config['PORT']))
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	s.bind(("localhost", config['PORT'])) 
	s.listen(1) 
	while True:
		print("Wait a connection")
		conn, addr = s.accept()
		print("Connection acepted") 
		try:
			thread.start_new_thread( respond, (conn,)) 
		except:
			print("Error: unable to start a thrread")
