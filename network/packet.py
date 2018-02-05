
class Packet:
	
	def __init__(self, type):
		self.__type = type
	
	def getType(self):
		return self.__type
	
	def writeData(self, stream):
		pass
	
	def readData(self, stream):
		pass
	
	def execute(self):
		pass