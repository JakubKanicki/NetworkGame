import random
import directions
from player import Player
from projectile import Projectile
from particle import Particle


class Map:
	
	def __init__(self, sizeX, sizeY):
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.players = []
		self.dPlayers = []
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
				tile = random.randrange(0, 10)
				if(tile >= 5):
					tile -= 5
				else:
					tile %= 2
				temp.append(tile)
			self.terrain.append(temp)
		self.players.append(Player(0, 0))
		self.players.append(Player(sizeX-1, sizeY-1))		#temporary
		self.clearArea(5, 5, 5)
		self.clearArea(sizeX-5, sizeY-5, 5)

	def update(self):
		self.updateGameObject(self.players, self.dPlayers)
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
		#	self.entities.append(Ent(x, y, type)) #TODO
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

	def getPlayer(self, x, y):
		for player in self.players:
			if(player.alive and player.x == x and player.y == y):
				return player
	
	def isSolid(self, x, y, isPlayer=False):
		if(not self.isValid(x, y)):
			return True
		tile = self.terrain[y][x]
		if(isPlayer):
			terr = tile == 0 or tile == 3
		else:
			terr = tile == 0 or tile == 2
		return not terr or self.getPlayer(x, y)
	
	def isValid(self, x, y):
		vx = x >= 0 and x < self.sizeX
		vy = y >= 0 and y < self.sizeY
		return  vx and vy

	def clearArea(self, x, y, rad):
		for i in range(-rad, rad):
			for j in range(-rad, rad):
				self.setTile(x + i, y + j, 0)

	def setTile(self, x, y, tile):
		if(self.isValid(x, y)):
			self.terrain[y][x] = tile

	def getTile(self, x, y):
		if(self.isValid(x, y)):
			return self.terrain[y][x]

	def getTopObject(self, x, y):
		gameObject = self.getPlayer(x, y)
		if not gameObject:
			gameObject = self.getProjectile(x, y)
			if not gameObject:
				gameObject = self.getEntity(x, y)
				if not gameObject:
					gameObject = self.getParticle(x, y)
		return gameObject

	def explode(self, x, y, power):
		self.spawnParticle(x, y, 0)
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
		tmp = self.getTile(x, y)
		if(tmp <= 1):
			self.setTile(x, y, 0)
			self.spawnParticle(x, y, 0)
		return tmp == 1 or tmp == 3 or tmp == 4