import socket
import io
import sys
from . import packetHandler
import logging


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
		logging.warning('Connection refused')
		return False

def recv(sock, buffer):
	data = None
	try:
		data = sock.recv(buffer)
	except ConnectionResetError:
		logging.warning('Connection reset')
	except ConnectionAbortedError:
		logging.warning('Connection aborted')
	return data

def send(sock, data):
	try:
		sock.send(data)
		return True
	except ConnectionResetError:
		logging.warning('Connection reset')
		return False

def sendPacket(sock, packet):
	stream = io.BytesIO()
	packetHandler.sendPacket(stream, packet)
	packetSize = sys.getsizeof(stream.getvalue())
	logging.info('Sending packet size info (%i)' % packetSize)
	if(not send(sock, packetSize.to_bytes(4, byteorder='big'))):
		return False
	return send(sock, stream.getvalue())

def recvPacket(sock):
	data = recv(sock, 4)
	if(not data):
		logging.warning('Connection lost')
		return None
	packetSize = int.from_bytes(data, byteorder='big')
	logging.info('Receiving packet (size %i)' % packetSize)
	data = recv(sock, packetSize)
	if(not data):
		logging.warning('Connection lost')
		return None
	stream = io.BytesIO(data)
	return packetHandler.receivePacket(stream)
