import os
import shared

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
				projectile = map.getProjectile(j, i)
				if(hasPlayer):
					self.__draw(self.playerChar[map.player.direction])
				elif(projectile != None):
					self.__draw(projectile.getChar())
				else:
					self.__draw(self.terrainChar[map.terrain[i][j]])
			self.__draw('\n')

		if(not shared.debugRender):
			os.system('cls')
		print(''.join(self.frameBuffer), end='')

	def __draw(self, value):
		self.frameBuffer.append(value)