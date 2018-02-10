
class Particle():
	chars = ['#', '*', '+', '-', ',']

	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.alive = True

	def update(self, map):
		if(self.type < 4):
			self.type += 1
		elif(self.type == 4):
			self.alive = False

	def getChar(self):
		return self.chars[self.type]