"XML XHTML HTML TEMPLATE module"
"Falta mostrar erros na templace"

import re
import types

class Template(file):
	def __init__(self, filename, dicio = {}):
		file.__init__(self, filename, "r")
		self.setVars(dicio)
		self.buffer = ""
		
	def setVars(self, d):
		self.outputVars = d
		
	def setDebug():
		pass
	
	def parse(self):
		def parseLoop(buf, outputVars):
			aux = []
			pos = 0
			bl = self.reBeginLoop.search(buf)
			while not bl is None:
				bl2 = self.reBeginLoop.search(buf, bl.end())
				el = self.reEndLoop.search(buf, bl.end())
				while (not bl2 is None) and  (bl2.start() < el.start()):
					bl2 = self.reBeginLoop.search(buf, bl2.end())
					el = self.reEndLoop.search(buf, el.end())
				
				aux.append(buf[pos:bl.start()])
				if outputVars.has_key(bl.groups()[0]):
					if type(outputVars[bl.groups()[0]]) == types.ListType or type(outputVars[bl.groups()[0]]) == types.TupleType:
						auxbuf = buf[bl.end():el.start()]
						auxbuf2 = ""
						i = 0
						for outputVars_ in outputVars[bl.groups()[0]]:
							outputVars_extended = outputVars_
							outputVars_extended['__I__'] = i 
							outputVars_extended['__MOD2__'] = i % 2
							outputVars_extended['__MOD3__'] = i % 3
							outputVars_extended['__MOD4__'] = i % 4
							outputVars_extended['__MOD5__'] = i % 5
							outputVars_extended['__MOD6__'] = i % 6
							outputVars_extended['__MOD7__'] = i % 7
							outputVars_extended['__MOD8__'] = i % 8
							outputVars_extended['__MOD9__'] = i % 9
							outputVars_extended['__MOD10__'] = i % 10
							auxbuf2 += innerParse(auxbuf, outputVars_extended)
						aux.append(auxbuf2)
				pos = el.end()
				bl = self.reBeginLoop.search(buf, el.end())
			aux.append(buf[pos:])
			if len(aux) > 0:
				buf = "".join(map(str, aux))
			return buf
			
		def innerParse(buf, outputVars):
			#print("innerParse:")
			#print("<---  " + str(buf))
			#print("<---  " +  str(outputVars))
			
			# Include
			for item in self.reInclude.finditer(buf):
				if outputVars.has_key(item.groups()[0]):
					buf_ = file(vars_[item.groups()[0]], "r").read()
					buf = buf[:item.start()] + innerParse(buf_, outputVars) + buff[item.end():]
			
			# Loop
			buf = parseLoop(buf, outputVars)
						
			# Var
			aux = []
			pos = 0
			for item in self.reVar.finditer(buf):
				aux.append(buf[pos:item.start()])
				if outputVars.has_key(item.groups()[0]):
					aux.append(outputVars[item.groups()[0]])
				pos = item.end()
			aux.append(buf[pos:])
			if len(aux) > 0:
				buf = "".join(map(str, aux))
			
			# If
			for item in self.reIf.finditer(buf):
				if outputVars.has_key(item.groups()[0]):
					if outputVars[item.groups()[0]]:
						buf = self.buffer[:item.start()] + buf[item.groups()[1]] + self.buffer[item.end():]
					else:
						buf = buf[:item.start()] + buf[item.end():]
					
			# If Else
			for item in self.reIfElse.finditer(buf):
				if outputVars.has_key(item.groups()[0]):
					if outputVars[item.groups()[0]]:
						buf = buf[:item.start()] + buf[item.groups()[1]] + buf[item.end():]
					else:
						buf = buf[:item.start()] + buf[item.groups()[2]] + buf[item.end():]
					
			#print("--->  " + str(buf))						
			return buf	
					
		self.buffer = self.read()
		self.reVar = re.compile('<\s*set\s+$(\w+?)\s*/\s*>', re.DOTALL)
		self.reIf = re.compile('<\s*if\s+$(\w+?)\s*>(.*?)<\s*/\s*if\s*>', re.DOTALL)
		self.reIfElse = re.compile('<\s*if\s+$(\w+?)\s*>(.*?)<\s*else\s*>(.*?)<\s*/\s*if\s*>', re.DOTALL)
		self.reBeginLoop = re.compile('<\s*foreach\s+ $(\w+?)\s*>', re.DOTALL)
		self.reEndLoop = re.compile('<\s*/\s*foreach\s*>', re.DOTALL)
		self.reInclude = re.compile('<\s*include\s+(\w+?)\s*/\s*>', re.DOTALL)
		
		self.buffer = innerParse(self.buffer, self.outputVars)
		
	def output(self):
		return self.buffer