import random
import directions
from player import Player
from projectile import Projectile

class Map():
	
	def __init__(self, sizeX, sizeY):
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.projectiles = []
		self.dProjectiles = []
		self.terrain = []
		for i in range(0, sizeY):
			temp = []
			for j in range(0, sizeX):
				temp.append(random.randrange(0, 3))
			self.terrain.append(temp)
		self.player = Player(0, 0)

	def update(self):
		for proj in self.projectiles:
			if(proj.alive):
				proj.update(self)
			elif(proj not in self.dProjectiles):
				self.dProjectiles.append(proj)

		for proj in self.dProjectiles:
			self.projectiles.remove(proj)
		self.dProjectiles.clear()

	def spawnProjectile(self, x, y, type, direction):
		self.projectiles.append(Projectile(x, y, type, direction))

	def getProjectile(self, x, y):
		for proj in self.projectiles:
			if(proj.alive and proj.x == x and proj.y == y):
				return proj
	
	def isSolid(self, x, y):
		if(not self.isValid(x, y)):
			return True
		return self.terrain[y][x] > 1 or (self.player.x == x and self.player.y == y)
	
	def isValid(self, x, y):
		vx = x >= 0 and x < self.sizeX
		vy = y >= 0 and y < self.sizeY
		return  vx and vy

	def setTile(self, x, y, tile):
		if(self.isValid(x, y)):
			self.terrain[y][x] = tile