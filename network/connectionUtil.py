import socket
import io
from . import packetHandler


def getSocket():
	return socket.socket(socket.AF_INET, socket.SOCK_STREAM)		# tcp socket.SOCK_STREAM; udp socket.SOCK_DGRAM

def bindServer(host, port):
	sock = getSocket()
	sock.bind((host, port))
	sock.listen(1)
	return sock

def connectClient(sock, host, port):
	try:
		sock.connect((host, port))
		return True
	except ConnectionRefusedError:
		print("Connection refused")
		return False

def recv(sock, buffer=1024):
	data = None
	try:
		data = sock.recv(buffer)
	except ConnectionResetError:
		print("Connection reset")
	except ConnectionAbortedError:
		print("Connection aborted")
	return data

def send(sock, data):
	try:
		sock.send(data)
		return True
	except ConnectionResetError:
		print("Connection reset")
		return False

def sendPacket(sock, packet):
	stream = io.BytesIO()
	packetHandler.sendPacket(stream, packet)
	return send(sock, stream.getvalue())

def recvPacket(sock, buffer=1024):
	data = recv(sock, buffer)
	if(not data):
		print("Connection lost")
		return None
	stream = io.BytesIO(data)
	return packetHandler.receivePacket(stream)
