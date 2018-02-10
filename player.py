from directions import Direction
import directions


class Player:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.direction = Direction.UP

	def move(self, map, direction):
		vec = directions.getVec(direction)
		if (not map.isSolid(self.x + vec[0], self.y + vec[1])):
			self.x += vec[0]
			self.y += vec[1]
		self.direction = direction