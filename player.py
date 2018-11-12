from directions import Direction
from network import streamUtil
import directions
import shared
import game
from network.packetPlayerMove import PacketPlayerMove


class Player:
	playerChar = ['^', 'v', '<', '>']
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.direction = Direction.UP
		self.alive = True

	def move(self, map, direction):
		vec = directions.getVec(direction)
		if (not map.isSolid(self.x + vec[0], self.y + vec[1], True)):
			self.x += vec[0]
			self.y += vec[1]
		self.direction = direction
		if(shared.isNetworked and not shared.isClient):
			game.networkHandler.queueOutbound(PacketPlayerMove(map.players.index(self), self))

	def writeToStream(self, stream):
		streamUtil.writeInt(stream, self.x, 1)
		streamUtil.writeInt(stream, self.y, 1)
		streamUtil.writeInt(stream, self.direction, 1)

	def readFromStream(self, stream):
		self.x = streamUtil.readInt(stream, 1)
		self.y = streamUtil.readInt(stream, 1)
		self.direction = streamUtil.readInt(stream, 1)

	def update(self, map):
		pass

	def getChar(self):
		return self.playerChar[self.direction]