from . import streamUtil
import logger


def sendPacket(stream, packet):
	streamUtil.writeInt(stream, packet.getType(), 1)
	packet.writeData(stream)
	return stream

def receivePacket(stream):
	id = streamUtil.readInt(stream, 1)
	logger.debug('Receiving packet with id: %i' % id)
	packet = buildPacket(id)
	packet.readData(stream)
	return packet


from .packetInvalid import PacketInvalid
from .packetKeyPressed import PacketKeyPressed
from .packetFullMapSync import PacketFullMapSync


def getPacketList():		# find a better way to do this
	packets = []
	packets.append(PacketInvalid)
	packets.append(PacketKeyPressed)
	packets.append(PacketFullMapSync)
	return packets

def buildPacket(id):
	packets = getPacketList()
	if id < len(packets):
		return packets[id]()
	return packets[0]()