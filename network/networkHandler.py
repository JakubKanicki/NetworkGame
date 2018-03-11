import time
from queue import Queue
from threading import Thread, Lock
import logger


class NetworkThread(Thread):	#TODO actually set this up as a server / client and check packet target

	def __init__(self, handler):
		Thread.__init__(self)
		self.setName('NETWORK_THREAD')
		self.handler = handler
		self.running = True
		self.setDaemon(True)#connection should be properly closed

	def run(self):#one day I hope to get rid of all debug calls in this file...
		self.debug('Starting thread')
		while self.running:
			packet = self.nextOutbound()
			while(packet != None):
				self.debug('Got packet')
				self.queueInbound(packet)
				packet = self.nextOutbound()
			time.sleep(0.01)
		self.debug('Exiting thread')

	def debug(self, val):
		logger.debug(self.getName() + '| ' + val, isDaemon=True)

	def nextOutbound(self):
		self.debug('Acquiring outbound lock...')
		self.handler.outboundLock.acquire()
		qsize = self.handler.outboundQueue.qsize()
		self.debug('Outbound lock acquired, queue size: ' + str(qsize))
		packet = None
		if (qsize > 0):
			packet = self.handler.outboundQueue.get()
			self.debug('Packet retrieved')
		self.handler.outboundLock.release()
		self.debug('Outbound lock released')
		return packet

	def queueInbound(self, packet):
		self.debug('Acquiring inbound lock...')
		self.handler.inboundLock.acquire()
		self.debug('Inbound lock acquired, queue size: ' + str(self.handler.inboundQueue.qsize()))
		self.handler.inboundQueue.put(packet)
		self.debug('Packet added to queue')
		self.handler.inboundLock.release()
		self.debug('Inbound lock released')
		return packet


class NetworkHandler:#possibly have separate threads for receiving and transmitting

	def __init__(self):
		self.inboundQueue = Queue(16)
		self.outboundQueue = Queue(16)
		self.inboundLock = Lock()
		self.outboundLock = Lock()
		self.networkThread = NetworkThread(self)

	def start(self):
		self.networkThread.start()

	def stop(self):
		self.networkThread.running = False

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
		self.outboundLock.acquire()
		logger.debug('Outbound lock acquired, queue size: ' + str(self.outboundQueue.qsize()))
		self.outboundQueue.put(packet)
		logger.debug('Packet added to queue')
		self.outboundLock.release()
		logger.debug('Outbound lock released')
		return packet
