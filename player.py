from directions import Direction

class Player():
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.direction = Direction.UP