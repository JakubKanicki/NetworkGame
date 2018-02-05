import socket
import io
import sys
from network.packetMessage import PacketMessage
from network import packetHandler

def main():
	host = 'localhost' #socket.gethostname() #if none then all available interfaces will be used
	port = 5000

	if(len(sys.argv)>1):
		host = sys.argv[1]
	if(len(sys.argv)>2):
		port = int(sys.argv[2])
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	
	s.listen(1)
	
	print("Listening on " + str(host) + "(" + str(socket.gethostbyname(host)) + ") on port " + str(port))
	
	conn, addr = s.accept()
	print("Connection from: " + str(addr))
	
	while True:
		try:
			data = conn.recv(1024)
		except ConnectionResetError:
			print("Connection reset")
			break
		if not data:
			print("Connection lost")
			break
		inStream = io.BytesIO(data)
		inPacket = packetHandler.receivePacket(inStream)
		inPacket.execute()

		print("Message from connected user: " + inPacket.msg)
		msg = inPacket.msg.upper()
		print("Sending message to user: " + msg)

		outStream = io.BytesIO()
		packetHandler.sendPacket(outStream, PacketMessage(msg))
		try:
			conn.send(outStream.getvalue())
		except ConnectionResetError:
			print("Connection reset")
			break
	conn.close()
	s.close()

if __name__ == '__main__':
	main()