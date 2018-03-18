from . import streamUtil


def sendPacket(stream, packet):
	streamUtil.writeInt(stream, packet.getType(), 1)
	packet.writeData(stream)
	return stream

def receivePacket(stream):
	id = streamUtil.readInt(stream, 1)
	packet = buildPacket(id)
	packet.readData(stream)
	return packet


from .packetInvalid import PacketInvalid
from .packetMessage import PacketMessage
from .packetKeyPressed import PacketKeyPressed

def getPacketList():		# find a better way to do this
	packets = []
	packets.append(PacketInvalid)
	packets.append(PacketMessage)
	packets.append(PacketKeyPressed)
	return packets

def buildPacket(id):
	packets = getPacketList()
	if id < len(packets):
		return packets[id]()
	return packets[0]()