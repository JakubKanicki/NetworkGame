import io
import sys
import os
from network import connectionManager
from network.packetMessage import PacketMessage
from network import packetHandler

def main():
	host = 'localhost'
	port = 5000

	if(len(sys.argv)>1):
		host = sys.argv[1]
	if(len(sys.argv)>2):
		port = int(sys.argv[2])

	sock = connectionManager.getSocket()
	while True:
		if(connectionManager.connectClient(sock, host, port)):
			break
		print("Press return to retry connection, enter 'q' to quit")
		if(input(">") == 'q'):
			sys.exit(0)

	print("Connected to server: " + str(sock.getpeername()))

	message = input(">")
	while message != 'q':
		if(not connectionManager.sendPacket(sock, PacketMessage(message))):
			break
		inPacket = connectionManager.recvPacket(sock)
		if(not inPacket):
			break
		inPacket.execute()
		print("Message from server: " + inPacket.msg)
		message = input(">")
	sock.close()
	os.system('pause')

if __name__ == '__main__':
	main()