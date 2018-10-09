import random
import shared
from player import Player
from projectile import Projectile
from particle import Particle
import game

class Map:
	
	def __init__(self, sizeX, sizeY):
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.players = []
		self.projectiles = []
		self.entities = []
		self.particles = []
		self.terrain = []
		self.isGenerated = False

	def generateRandom(self):
		for i in range(0, self.sizeY):
			temp = []
			for j in range(0, self.sizeX):
				tile = random.randrange(0, 10)
				if(tile >= 5):
					tile -= 5
				else:
					tile %= 2
				temp.append(tile)
			self.terrain.append(temp)

	def generateMap(self):
		self.generateRandom()
		self.players.append(Player(0, 0))
		self.clearArea(5, 5, 5)
		self.players.append(Player(self.sizeX - 1, self.sizeY - 1))  # temporary
		self.clearArea(self.sizeX - 5, self.sizeY - 5, 5)
		self.isGenerated = True

	def update(self):
		if(not self.isGenerated):
			if(shared.isNetworked and shared.isClient):
				from network.packetClientRequest import PacketClientRequest
				game.networkHandler.queueOutbound(PacketClientRequest(PacketClientRequest.REQ_FULL_MAP_SYNC))
			self.generateMap()
		self.updateGameObjects(self.players)
		self.updateGameObjects(self.projectiles)
		self.updateGameObjects(self.entities)
		self.updateGameObjects(self.particles)

	def updateGameObjects(self, list):
		dList = []

		for obj in list:
			if(obj.alive):
				obj.update(self)
			elif(obj not in dList):
				dList.append(obj)

		for obj in dList:
			list.remove(obj)

	def getGameObject(self, x, y, list):
		for obj in list:
			if(obj.alive and obj.x == x and obj.y == y):
				return obj

	def spawnProjectile(self, x, y, type, direction):
		if(self.isValid(x, y)):
			self.projectiles.append(Projectile(x, y, type, direction))

	def getProjectile(self, x, y):
		return self.getGameObject(x, y, self.projectiles)

	# def spawnEntity(self, x, y, type):	# TODO make entity class
	# 	if(self.isValid(x, y)):
	# 		self.entities.append(Ent(x, y, type))

	def getEntity(self, x, y):
		return self.getGameObject(x, y, self.entities)

	def spawnParticle(self, x, y, type):
		if(self.isValid(x, y)):
			self.particles.insert(0, Particle(x, y, type))

	def getParticle(self, x, y):
		return self.getGameObject(x, y, self.particles)

	def spawnPlayer(self, x, y):
		if(self.isValid(x, y)):
			self.players.append(Player(x, y))

	def getPlayer(self, x, y):
		return self.getGameObject(x, y, self.players)
	
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
		return vx and vy

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