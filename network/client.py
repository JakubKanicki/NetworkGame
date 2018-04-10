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
		self.queue = Queue(16)
		self.lock = Lock()
		self.running = True
		self.setDaemon(True)		# connection should be properly closed
		self.sock = connectionUtil.getSocket()
		while True:
			if (connectionUtil.connectClient(self.sock, shared.host, shared.port+1)):
				break
			time.sleep(0.5)

	def run(self):
		self.debug('Starting thread')
		while self.running:
			packet = self.nextOutbound()
			while(packet != None):
				self.debug('Got packet')
				if(not connectionUtil.sendPacket(self.sock, packet)):
					self.debug('FAILED TO SEND PACKET')
				packet = self.nextOutbound()
			time.sleep(0.01)
		self.sock.close()
		self.debug('Exiting thread')

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


class InboundThread(Thread):		# TODO check packet side

	def __init__(self):
		Thread.__init__(self)
		self.setName('INBOUND_NETWORK_THREAD')
		self.queue = Queue(16)
		self.lock = Lock()
		self.running = True
		self.setDaemon(True)		# connection should be properly closed
		self.sock = connectionUtil.getSocket()
		while True:
			if (connectionUtil.connectClient(self.sock, shared.host, shared.port)):
				break
			time.sleep(0.5)

	def run(self):
		self.debug('Starting thread')
		while self.running:
			packet = connectionUtil.recvPacket(self.sock)
			if (not packet):
				self.debug('FAILED TO RECEIVE PACKET')
				continue
			self.debug('Got packet')
			self.queueInbound(packet)
			# time.sleep(0.01)
		self.sock.close()
		self.debug('Exiting thread')

	def debug(self, val):
		logger.debug(self.getName() + '| ' + val, isDaemon=True)

	def queueInbound(self, packet):
		self.debug('Acquiring inbound lock...')
		self.lock.acquire()
		self.debug('Inbound lock acquired, queue size: ' + str(self.queue.qsize()))
		self.queue.put(packet)
		self.debug('Packet added to queue')
		self.lock.release()
		self.debug('Inbound lock released')
		return packet


class NetworkHandler:

	def __init__(self):
		self.inboundThread = InboundThread()
		self.outboundThread = OutboundThread()

	def start(self):
		self.inboundThread.start()
		self.outboundThread.start()

	def stop(self):
		self.inboundThread.running = False
		self.outboundThread.running = False

	def nextInbound(self):
		logger.debug('Acquiring inbound lock...')
		self.inboundThread.lock.acquire()
		qsize = self.inboundThread.queue.qsize()
		logger.debug('Inbound lock acquired, queue size: ' + str(qsize))
		packet = None
		if (qsize > 0):
			packet = self.inboundThread.queue.get()
			logger.debug('Packet retrieved')
		self.inboundThread.lock.release()
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
