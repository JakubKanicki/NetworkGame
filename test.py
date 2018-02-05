import io
import sys
from network import packetMessage
from network import packetHandler

msg = 'HALOE!'

if(len(sys.argv)>1):
	msg = sys.argv[1]

packet = packetMessage.PacketMessage(msg)
packet.execute()

stream = io.BytesIO()
packetHandler.sendPacket(stream, packet)

value = stream.getvalue()
print(value)

stream2 = io.BytesIO(value)
packet2 = packetHandler.receivePacket(stream2)

packet2.execute()

print(packet.getType())
