import random
import directions
from player import Player
from projectile import Projectile
from particle import Particle

class Map():
	
	def __init__(self, sizeX, sizeY):
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.projectiles = []
		self.dProjectiles = []
		self.entities = []
		self.dEntities = []
		self.particles = []
		self.dParticles = []
		self.terrain = []
		for i in range(0, sizeY):
			temp = []
			for j in range(0, sizeX):
				temp.append(random.randrange(0, 3))
			self.terrain.append(temp)
		self.player = Player(0, 0)

	def update(self):
		self.updateGameObject(self.projectiles, self.dProjectiles)
		self.updateGameObject(self.entities, self.dEntities)
		self.updateGameObject(self.particles, self.dParticles)

	def updateGameObject(self, list, dList):
		for obj in list:
			if(obj.alive):
				obj.update(self)
			elif(obj not in dList):
				dList.append(obj)

		for obj in dList:
			list.remove(obj)
		dList.clear()

	def spawnProjectile(self, x, y, type, direction):
		if(self.isValid(x, y)):
			self.projectiles.append(Projectile(x, y, type, direction))

	def getProjectile(self, x, y):
		for proj in self.projectiles:
			if(proj.alive and proj.x == x and proj.y == y):
				return proj

	def spawnEntity(self, x, y, type):
		#if(self.isValid(x, y)):
		#	self.entities.append(Projectile(x, y, type)) #TODO
		pass

	def getEntity(self, x, y):
		for ent in self.entities:
			if(ent.alive and ent.x == x and ent.y == y):
				return ent

	def spawnParticle(self, x, y, type):
		if(self.isValid(x, y)):
			self.particles.insert(0, Particle(x, y, type))

	def getParticle(self, x, y):
		for part in self.particles:
			if(part.alive and part.x == x and part.y == y):
				return part
	
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

	def getTile(self, x, y):
		if(self.isValid(x, y)):
			return self.terrain[y][x]

	def explode(self, x, y, power):
		if(self.__expl(x, y)):
			return
		for i in range(0, power):
			if(self.__expl(x, y-i)):
				break
		for i in range(0, power):
			if(self.__expl(x, y+i)):
				break
		for i in range(0, power):
			if(self.__expl(x-i, y)):
				break
		for i in range(0, power):
			if(self.__expl(x+i, y)):
				break

	def __expl(self, x, y):
		if(not self.isValid(x, y)):
			return True
		tmp = self.getTile(x, y) > 1
		self.setTile(x, y, 0)
		self.spawnParticle(x, y, 0)
		return tmp