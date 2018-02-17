import time
from queue import Queue
from threading import Thread, Lock
import logger

class NetworkThread(Thread):

	def __init__(self, handler):
		Thread.__init__(self)
		self.setName('NETWORK_THREAD')
		self.handler = handler
		self.running = True
		#self.setDaemon(True) connection should be properly closed

	def run(self):
		self.debug('Starting thread')
		while self.running:
			time.sleep(1)
			self.debug('Tick, I exist.')
		self.debug('Exiting thread')

	def debug(self, val):
		logger.debug(self.getName() + '| ' + val)


class NetworkHandler:

	def __init__(self, isServer):
		self.inboundQueue = Queue(16)
		self.outboundQueue = Queue(16)
		self.inboundLock = Lock()
		self.outboundLock = Lock()
		self.networkThread = NetworkThread(self)
		self.isServer = isServer

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
		if(qsize > 0):
			packet = self.inboundQueue.get()
			logger.debug('Packet retrieved')
		self.inboundLock.release()
		logger.debug('Inbound lock released')
		return packet

	def sendOutbound(self, packet):
		logger.debug('Acquiring outbound lock...')
		self.outboundLock.acquire()
		logger.debug('Outbound lock acquired, queue size: ' + str(self.outboundQueue.qsize()))
		self.outboundQueue.put(packet)
		logger.debug('Packet added to queue')
		self.outboundLock.release()
		logger.debug('Outbound lock released')
		return packet