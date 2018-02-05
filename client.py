import socket
import io
import sys
from network.packetMessage import PacketMessage
from network import packetHandler

def main():
	host = 'localhost'
	port = 5000
	connected = False

	if(len(sys.argv)>1):
		host = sys.argv[1]
	if(len(sys.argv)>2):
		port = int(sys.argv[2])
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp socket.SOCK_STREAM; udp socket.SOCK_DGRAM

	while True:
		try:
			s.connect((host, port))
			connected = True
		except ConnectionRefusedError:
			pass
		if connected:
			break
		print("Connection refused")
		print("Press return to retry connection, enter 'q' to quit")
		if(input(">") == 'q'):
			sys.exit(0)

	print("Connected to server: " + str(s.getpeername()))

	message = input(">")
	while message != 'q':
		outPacket = PacketMessage(message)
		outStream = io.BytesIO()
		packetHandler.sendPacket(outStream, outPacket)
		try:
			s.send(outStream.getvalue())
		except ConnectionResetError:
			print("Connection reset")
			break

		try:
			data = s.recv(1024)
		except ConnectionResetError:
			print("Connection reset")
			break
		inStream = io.BytesIO(data)
		inPacket = packetHandler.receivePacket(inStream)
		inPacket.execute()
		print("Message from server: " + inPacket.msg)
		message = input(">")
	s.close()

if __name__ == '__main__':
	main()