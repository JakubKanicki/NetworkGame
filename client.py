import sys
import os
from network import connectionUtil
from network.packetMessage import PacketMessage


def main():
	host = 'localhost'
	port = 5000

	if(len(sys.argv)>1):
		host = sys.argv[1]
	if(len(sys.argv)>2):
		port = int(sys.argv[2])

	sock = connectionUtil.getSocket()
	while True:
		if(connectionUtil.connectClient(sock, host, port)):
			break
		print("Press return to retry connection, enter 'q' to quit")
		if(input(">") == 'q'):
			sys.exit(0)

	print("Connected to server: " + str(sock.getpeername()))

	message = input(">")
	while message != 'q':
		if(not connectionUtil.sendPacket(sock, PacketMessage(message))):
			break
		inPacket = connectionUtil.recvPacket(sock)
		if(not inPacket):
			break
		inPacket.execute()
		print("Message from server: " + inPacket.msg)
		message = input(">")
	sock.close()
	os.system('pause')


if __name__ == '__main__':
	main()