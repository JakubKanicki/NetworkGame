import directions

class Projectile():
	shell = ['n', 'u', '{', '}']

	def __init__(self, x, y, type, direction):
		self.x = x
		self.y = y
		self.type = type
		self.direction = direction

	def update(self, map):
		if(self.type == 0):
			vec = directions.getMovement(self.direction)

			for i in range(0, 8):
				if(not map.isSolid(self.x + vec[0], self.y + vec[1])):
					self.x += vec[0]
					self.y += vec[1]
				else:
					map.setTile(self.x + vec[0], self.y + vec[1], 0)

	def getChar(self):
		return self.shell[self.direction]