import os
import platform
import shared
import logging


class Renderer:
	terrainChar = [' ', '#', '~', 'O', '@']
	clearCall = 'cls' if (platform.system() == 'Windows') else 'clear'

	def __init__(self):
		self.frameBuffer = []

	def render(self, map):
		if(not shared.enableRender):
			return
		self.frameBuffer = []

		self.__draw('P: %i NE: %i\n' % (len(map.projectiles), shared.invalidPacketCount))

		for i in range(0, map.sizeY):
			for j in range(0, map.sizeX):
				obj = map.getTopObject(j, i)
				if(obj):
					self.__draw(obj.getChar())
				else:
					self.__draw(self.terrainChar[map.getTile(j, i)])
			self.__draw('\n')

		if(not shared.debugRender):
			logging.debug('-RENDER-%s-' % self.clearCall.upper())
			os.system(self.clearCall)
		logging.debug('Printing')
		print(''.join(self.frameBuffer), end='')

	def __draw(self, value):
		self.frameBuffer.append(value)