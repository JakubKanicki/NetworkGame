import os
import shared
import logger


class Renderer():
	terrainChar = ['.', ',', '#']
	playerChar = ['^', 'v', '<', '>']

	def __init__(self):
		self.frameBuffer = []

	def render(self, map):
		self.frameBuffer = []

		self.__draw('P: ' + str(len(map.projectiles)) + '\n')

		for i in range(0, map.sizeY):
			for j in range(0, map.sizeX):
				hasPlayer = j == map.player.x and i == map.player.y
				proj = map.getProjectile(j, i)
				ent = map.getEntity(j, i)
				part = map.getParticle(j, i)
				if(hasPlayer):
					self.__draw(self.playerChar[map.player.direction])
				elif(proj != None):
					self.__draw(proj.getChar())
				elif(ent != None):
					self.__draw(ent.getChar())
				elif(part != None):
					self.__draw(part.getChar())
				else:
					self.__draw(self.terrainChar[map.getTile(j, i)])
			self.__draw('\n')

		if(not shared.debugRender):
			logger.debug('-RENDER-CLS-')
			os.system('cls')
		logger.debug('-PRINTING-')
		print(''.join(self.frameBuffer), end='')

	def __draw(self, value):
		self.frameBuffer.append(value)