import socket
import sys
import os
from network import connectionUtil
from network.packetMessage import PacketMessage


def main():
	host = 'localhost' # socket.gethostname() or if none then all available interfaces will be used
	port = 5000

	if(len(sys.argv)>1):
		host = sys.argv[1]
	if(len(sys.argv)>2):
		port = int(sys.argv[2])

	sock = connectionUtil.bindServer(host, port)
	
	print("Listening on %s (%s) on port %i" % (host, socket.gethostbyname(host), port))
	
	conn, addr = sock.accept()
	print("Connection from: " + str(addr))
	
	while True:
		inPacket = connectionUtil.recvPacket(conn)
		if(not inPacket):
			break
		inPacket.execute()

		print("Message from connected user: " + inPacket.msg)
		msg = inPacket.msg.upper()
		print("Sending message to user: " + msg)

		if(not connectionUtil.sendPacket(conn, PacketMessage(msg))):
			break
	conn.close()
	sock.close()
	os.system('pause')


if __name__ == '__main__':
	main()