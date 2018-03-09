import os
import shared
import logger


class Renderer:
	terrainChar = [' ', '#', '~', 'O', '@']

	def __init__(self):
		self.frameBuffer = []

	def render(self, map):
		self.frameBuffer = []

		self.__draw('P: ' + str(len(map.projectiles)) + '\n')

		for i in range(0, map.sizeY):
			for j in range(0, map.sizeX):
				obj = map.getTopObject(j, i)
				if(obj):
					self.__draw(obj.getChar())
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