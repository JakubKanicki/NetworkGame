import time
from queue import Queue
from threading import Thread, Lock
from . import connectionUtil
import shared
import logger

# TODO implement close in all of these & on the client
class OutboundThread(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.setName('OUTBOUND_NETWORK_THREAD')
		self.queue = Queue(32)
		self.lock = Lock()
		self.running = True
		self.setDaemon(True)		# connection should be properly closed
		self.clients = []		# TODO implement a safe way of adding clients (another lock)

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


class InboundThread(Thread):		# TODO check packet target

	def __init__(self, handler, client):
		Thread.__init__(self)
		self.setName('INBOUND_NETWORK_THREAD')		# TODO add id to name
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
		self.client[1].close()
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


# TODO create client discovery thread
# TODO create accept method which will create client connections and either create new inbound threads as well as add clients to outbound thread or queue that for main thread to manage on engine update
# maybe do it on engine update, seems safer to create new threads using the main one, although it would still require additional locks for outbound thread, but not for itself


class NetworkHandler:

	def __init__(self):
		self.outboundThread = OutboundThread()
		self.inboundThreads = []		# TODO add lock for new inbound threads
		self.inboundQueue = Queue(32)
		self.inboundLock = Lock()

	def start(self):		# TODO start discovery thread
		self.outboundThread.start()

	def stop(self):
		self.outboundThread.running = False
		for inboundThread in self.inboundThreads:
			inboundThread.running = False

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
