import time
from queue import Queue
from threading import Thread, Lock
from . import connectionUtil
import shared
import logger


class OutboundThread(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.setName('OUTBOUND_NETWORK_THREAD')
		self.queue = Queue(32)
		self.lock = Lock()
		self.running = True
		self.setDaemon(True)
		self.clients = []
		self.discoveryLock = Lock()


	def run(self):
		self.debug('Starting thread')
		while self.running:
			packet = self.nextOutbound()
			while(packet != None):
				self.debug('Got packet')
				self.routePacket(packet)
				packet = self.nextOutbound()
			time.sleep(0.01)
		for client in self.clients:
			client[1].close()
		self.debug('Exiting thread')

	def routePacket(self, packet):
		if (packet.clientId < 0):
			for client in self.clients:
				self.send(client, packet)
		else:
			for client in self.clients:
				if (client[0] == packet.clientId):
					self.send(client, packet)
					break

	def send(self, client, packet):
		if (not connectionUtil.sendPacket(client[1], packet)):
			self.debug('FAILED TO SEND PACKET TO CLIENT #%i' % client[0])		# TODO implement client dropping on fail (maybe retry a few times)

	def debug(self, val):
		logger.debug(self.getName() + '| ' + val, isDaemon=True)

	def nextOutbound(self):
		self.debug('Acquiring outbound lock...')
		self.lock.acquire()
		qsize = self.queue.qsize()
		self.debug('Outbound lock acquired, queue size: ' + str(qsize))
		packet = None
		if (qsize > 0):
			packet = self.queue.get()
			self.debug('Packet retrieved')
		self.lock.release()
		self.debug('Outbound lock released')
		return packet

	def stop(self):
		self.debug('Stopping...')
		self.discoveryLock.acquire()
		for client in self.clients:
			client[1].close()
		self.discoveryLock.release()
		self.running = False


class InboundThread(Thread):		# TODO check packet target

	def __init__(self, handler, client):
		Thread.__init__(self)
		self.setName('INBOUND_NETWORK_THREAD_'+str(client[0]))
		self.running = True
		self.setDaemon(True)		# connection should be properly closed
		self.handler = handler
		self.client = client		# client (id, socket, ip)

	def run(self):
		self.debug('Starting thread')
		while self.running:
			packet = connectionUtil.recvPacket(self.client[1])
			if (not packet):
				self.debug('FAILED TO RECEIVE PACKET')		# TODO implement client dropping on fail (maybe retry a few times)
				continue
			self.debug('Got packet')
			packet.clientId = self.client[0]
			self.queueInbound(packet)
		self.debug('Exiting thread')

	def debug(self, val):
		logger.debug(self.getName() + '| ' + val, isDaemon=True)

	def queueInbound(self, packet):
		self.debug('Acquiring inbound lock...')
		self.handler.inboundLock.acquire()
		self.debug('Inbound lock acquired, queue size: ' + str(self.handler.inboundQueue.qsize()))
		self.handler.inboundQueue.put(packet)
		self.debug('Packet added to queue')
		self.handler.inboundLock.release()
		self.debug('Inbound lock released')
		return packet

	def stop(self):
		self.debug('Stopping...')
		self.client[1].close()
		self.running = False


class DiscoveryThread(Thread):

	def __init__(self, handler):
		Thread.__init__(self)
		self.setName('DISCOVERY_NETWORK_THREAD')
		self.running = True
		self.setDaemon(True)
		self.handler = handler
		self.inSock = connectionUtil.bindServer(shared.host, shared.port+1)
		self.outSock = connectionUtil.bindServer(shared.host, shared.port)
		self.lastClientId = 0

	def run(self):
		self.debug('Starting thread')
		while self.running:
			self.lastClientId += 1
			clientIn = self.accept(self.inSock, self.lastClientId)
			clientOut = self.accept(self.outSock, self.lastClientId)		# possible extremely rare case when 2 clients connect simultaneously
			self.debug('Creating inbound thread for client #' + str(self.lastClientId))
			threadIn = InboundThread(self.handler, clientIn)
			self.debug('Acquiring handler discovery lock')
			self.handler.discoveryLock.acquire()
			self.handler.inboundThreads.append(threadIn)
			self.handler.discoveryLock.release()
			self.debug('Handler discovery lock released')
			threadIn.start()
			self.debug('Acquiring outbound discovery lock')
			self.handler.outboundThread.discoveryLock.acquire()
			self.handler.outboundThread.clients.append(clientOut)		# TODO test this whole thing
			self.handler.outboundThread.discoveryLock.release()
			self.debug('Outbound discovery lock released')
		self.debug('Exiting thread')

	def accept(self, sock, id):
		conn, addr = sock.accept()
		self.debug('Connection from: ' + str(addr))
		return [id, conn, addr]

	def debug(self, val):
		logger.debug(self.getName() + '| ' + val, isDaemon=True)

	def stop(self):
		self.debug('Stopping...')
		self.inSock.close()
		self.outSock.close()
		self.running = False


class NetworkHandler:

	def __init__(self):
		self.discoveryThread = DiscoveryThread(self)
		self.outboundThread = OutboundThread()
		self.inboundThreads = []
		self.inboundQueue = Queue(32)
		self.inboundLock = Lock()
		self.discoveryLock = Lock()

	def start(self):
		self.discoveryThread.start()
		self.outboundThread.start()

	def stop(self):
		logger.debug('Stopping network handler...')
		self.discoveryThread.stop()
		self.outboundThread.stop()
		self.discoveryLock.acquire()
		for inboundThread in self.inboundThreads:
			inboundThread.stop()
		self.discoveryLock.release()

	def nextInbound(self):
		logger.debug('Acquiring inbound lock...')
		self.inboundLock.acquire()
		qsize = self.inboundQueue.qsize()
		logger.debug('Inbound lock acquired, queue size: ' + str(qsize))
		packet = None
		if (qsize > 0):
			packet = self.inboundQueue.get()
			logger.debug('Packet retrieved')
		self.inboundLock.release()
		logger.debug('Inbound lock released')
		return packet

	def queueOutbound(self, packet):
		logger.debug('Acquiring outbound lock...')
		self.outboundThread.lock.acquire()
		logger.debug('Outbound lock acquired, queue size: ' + str(self.outboundThread.queue.qsize()))
		self.outboundThread.queue.put(packet)
		logger.debug('Packet added to queue')
		self.outboundThread.lock.release()
		logger.debug('Outbound lock released')
		return packet
