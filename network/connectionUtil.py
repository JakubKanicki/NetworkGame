import socket
import io
from . import packetHandler
import logger

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
		logger.debug("Connection refused")
		return False

def recv(sock, buffer=1024):
	data = None
	try:
		data = sock.recv(buffer)
	except ConnectionResetError:
		logger.debug("Connection reset")
	except ConnectionAbortedError:
		logger.debug("Connection aborted")
	return data

def send(sock, data):
	try:
		sock.send(data)
		return True
	except ConnectionResetError:
		logger.debug("Connection reset")
		return False

def sendPacket(sock, packet):
	stream = io.BytesIO()
	packetHandler.sendPacket(stream, packet)
	return send(sock, stream.getvalue())

def recvPacket(sock, buffer=10240):
	data = recv(sock, buffer)
	if(not data):
		logger.debug("Connection lost")
		return None
	stream = io.BytesIO(data)
	return packetHandler.receivePacket(stream)
