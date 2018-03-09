import socket
import sys
import os
from network import connectionManager
from network.packetMessage import PacketMessage


def main():
	host = 'localhost' #socket.gethostname() #if none then all available interfaces will be used
	port = 5000

	if(len(sys.argv)>1):
		host = sys.argv[1]
	if(len(sys.argv)>2):
		port = int(sys.argv[2])

	sock = connectionManager.bindServer(host, port)
	
	print("Listening on " + str(host) + "(" + str(socket.gethostbyname(host)) + ") on port " + str(port))
	
	conn, addr = sock.accept()
	print("Connection from: " + str(addr))
	
	while True:
		inPacket = connectionManager.recvPacket(conn)
		if(not inPacket):
			break
		inPacket.execute()

		print("Message from connected user: " + inPacket.msg)
		msg = inPacket.msg.upper()
		print("Sending message to user: " + msg)

		if(not connectionManager.sendPacket(conn, PacketMessage(msg))):
			break
	conn.close()
	sock.close()
	os.system('pause')


if __name__ == '__main__':
	main()