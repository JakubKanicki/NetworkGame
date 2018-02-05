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

def getPacketList(): #python was being retarded with cyclic imports so I had to remove classes from enum and separate the file, might as well just get rid of enum and replace it with a number
	packets = []
	packets.append(PacketInvalid)
	packets.append(PacketMessage)
	return packets

def buildPacket(id):
	packets = getPacketList()
	if id < len(packets):
		return packets[id]()
	return packets[0]()