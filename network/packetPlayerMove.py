from .packet import Packet
from .packetType import PacketType
from . import streamUtil


class PacketPlayerMove(Packet):

	def __init__(self, player_id=-1, player=None):
		super().__init__(PacketType.PLAYER_MOVE)
		self.player_id = player_id
		self.player = player

	def writeData(self, stream):
		streamUtil.writeInt(stream, self.player_id, 1)
		self.player.writeToStream(stream)

	def readData(self, stream):
		self.player_id = streamUtil.readInt(stream, 1)
		from player import Player
		self.player = Player(0, 0)
		self.player.readFromStream(stream)

	def execute(self, map):
		if(len(map.players) <= self.player_id):
			return
		map.players[self.player_id] = self.player
