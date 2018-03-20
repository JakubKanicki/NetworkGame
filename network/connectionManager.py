import time
from . import connectionUtil
import logger


class Connection:		# is there even a point in using interfaces in python?

	def __init__(self, host, port):
		pass

	def send(self, packet):
		pass

	def recv(self):
		pass

	def close(self):
		pass


class Client(Connection):

	def __init__(self, host, port):
		logger.debug('Client starting host %s, port %i' % (host, port))
		self.sock = connectionUtil.getSocket()
		while True:
			if (connectionUtil.connectClient(self.sock, host, port)):
				break
			time.sleep(0.5)
			# print("Press return to retry connection, enter 'q' to quit")
			# if (input(">") == 'q'):
			# 	sys.exit(0)

	def send(self, packet):
		return connectionUtil.sendPacket(self.sock, packet)

	def recv(self):
		return connectionUtil.recvPacket(self.sock)

	def close(self):
		self.sock.close()


import game		# temporary
from network.packetFullMapSync import PacketFullMapSync

class Server(Connection):		# should have separate files for server & client stuff

	def __init__(self, host, port):
		logger.debug('Server starting host %s, port %i' % (host, port))
		self.sock = connectionUtil.bindServer(host, port)
		self.clients = []

	def scan(self):
		conn, addr = self.sock.accept()
		logger.debug('Connection from: ' + str(addr))
		self.clients.append((conn, addr))
		game.networkHandler.queueOutbound(PacketFullMapSync(game.map))		# temporary

	def send(self, packet):		# TODO rename this sendAll & make method to send to individual clients
		if(len(self.clients) <= 0):
			self.scan()
		dClients = []
		for client in self.clients:
			if(not connectionUtil.sendPacket(client[0], packet)):
				dClients.append(client)
		self.dropClients(dClients)

	def recv(self):		# should probably have multiple threads for multiple clients...
		if(len(self.clients) <= 0):
			self.scan()
		dClients = []
		for client in self.clients:
			packet = connectionUtil.recvPacket(client[0])		# temporary
			if(not packet):
				dClients.append(client)
			return packet		# temporary
		self.dropClients(dClients)

	def dropClients(self, dClients):
		for client in dClients:
			logger.debug('Removing client IP ' + client[1])
			client[0].close()
			self.clients.remove(client)

	def close(self):
		for client in self.clients:
			client[0].close()
		self.sock.close()


def getConnection(isClient, host, port, isRecv):
	if(isClient):
		return Client(host, port if isRecv else port + 1)
	return Server(host, port + 1 if isRecv else port)