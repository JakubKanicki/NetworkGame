from directions import Direction
import directions


class Player:
	playerChar = ['^', 'v', '<', '>']
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.direction = Direction.UP
		self.alive = True

	def move(self, map, direction):
		vec = directions.getVec(direction)
		if (not map.isSolid(self.x + vec[0], self.y + vec[1], True)):
			self.x += vec[0]
			self.y += vec[1]
		self.direction = direction

	def update(self, map):
		pass

	def getChar(self):
		return self.playerChar[self.direction]