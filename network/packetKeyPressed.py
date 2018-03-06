from .packet import Packet
from .packetType import PacketType
from . import streamUtil
from directions import Direction
from keys import Key
import logger

class PacketKeyPressed(Packet):

	def __init__(self, keyId=None):
		super().__init__(PacketType.KEY_PRESSED)
		self.keyId = keyId

	def writeData(self, stream):
		streamUtil.writeInt(stream, self.keyId, 1)

	def readData(self, stream):
		self.keyId = streamUtil.readInt(stream, 1)

	def execute(self, map):
		logger.debug('Executing packet key pressed: %d' % self.keyId)
		if (self.keyId == Key.UP):
			map.players[0].move(map, Direction.UP)
		elif (self.keyId == Key.DOWN):
			map.players[0].move(map, Direction.DOWN)
		elif (self.keyId == Key.LEFT):
			map.players[0].move(map, Direction.LEFT)
		elif (self.keyId == Key.RIGHT):
			map.players[0].move(map, Direction.RIGHT)
		elif (self.keyId == Key.FIRE):
			map.spawnProjectile(map.players[0].x, map.players[0].y, 0, map.players[0].direction)

		elif (self.keyId == Key.DUP):
			map.players[1].move(map, Direction.UP)
		elif (self.keyId == Key.DDOWN):
			map.players[1].move(map, Direction.DOWN)
		elif (self.keyId == Key.DLEFT):
			map.players[1].move(map, Direction.LEFT)
		elif (self.keyId == Key.DRIGHT):
			map.players[1].move(map, Direction.RIGHT)
		elif (self.keyId == Key.DFIRE):
			map.spawnProjectile(map.players[1].x, map.players[1].y, 0, map.players[1].direction)