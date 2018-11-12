import time
from queue import Queue
from threading import Thread, Lock
from . import connectionUtil
import shared
import logging


class OutboundThread(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.setName('OUTBOUND_NETWORK_THREAD')
		self.queue = Queue(16)
		self.lock = Lock()
		self.running = True
		self.setDaemon(True)
		self.sock = connectionUtil.getSocket()
		while True:
			if (connectionUtil.connectClient(self.sock, shared.host, shared.port+1)):
				break
			time.sleep(0.5)

	def run(self):
		logging.info('Starting thread')
		while self.running:
			packet = self.nextOutbound()
			while(packet != None):
				logging.debug('Got packet')
				if(not connectionUtil.sendPacket(self.sock, packet)):
					logging.warning('FAILED TO SEND PACKET')
				packet = self.nextOutbound()
			time.sleep(0.01)
		logging.debug('Exiting thread')

	def nextOutbound(self):
		logging.debug('Acquiring outbound lock...')
		self.lock.acquire()
		qsize = self.queue.qsize()
		logging.debug('Outbound lock acquired, queue size: ' + str(qsize))
		packet = None
		if (qsize > 0):
			packet = self.queue.get()
			logging.debug('Packet retrieved')
		self.lock.release()
		logging.debug('Outbound lock released')
		return packet

	def stop(self):
		logging.info('Stopping...')
		self.sock.close()
		self.running = False


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
				# print('A'*20)
				break
			time.sleep(0.5)

	def run(self):
		logging.info('Starting thread')
		while self.running:
			packet = connectionUtil.recvPacket(self.sock)
			if (not packet):
				logging.warning('FAILED TO RECEIVE PACKET')
				continue
			logging.debug('Got packet')
			self.queueInbound(packet)
		logging.info('Exiting thread')

	def queueInbound(self, packet):
		logging.debug('Acquiring inbound lock...')
		self.lock.acquire()
		logging.debug('Inbound lock acquired, queue size: ' + str(self.queue.qsize()))
		self.queue.put(packet)
		logging.debug('Packet added to queue')
		self.lock.release()
		logging.debug('Inbound lock released')
		return packet

	def stop(self):
		logging.info('Stopping...')
		self.sock.close()
		self.running = False


class NetworkHandler:

	def __init__(self):
		self.inboundThread = InboundThread()
		self.outboundThread = OutboundThread()

	def start(self):
		self.inboundThread.start()
		self.outboundThread.start()

	def stop(self):
		logging.info('Stopping network handler...')
		self.inboundThread.stop()
		self.outboundThread.stop()

	def nextInbound(self):
		logging.debug('Acquiring inbound lock...')
		self.inboundThread.lock.acquire()
		qsize = self.inboundThread.queue.qsize()
		logging.debug('Inbound lock acquired, queue size: ' + str(qsize))
		packet = None
		if (qsize > 0):
			packet = self.inboundThread.queue.get()
			logging.debug('Packet retrieved')
		self.inboundThread.lock.release()
		logging.debug('Inbound lock released')
		return packet

	def queueOutbound(self, packet):
		logging.debug('Acquiring outbound lock...')
		self.outboundThread.lock.acquire()
		logging.debug('Outbound lock acquired, queue size: ' + str(self.outboundThread.queue.qsize()))
		self.outboundThread.queue.put(packet)
		logging.debug('Packet added to queue')
		self.outboundThread.lock.release()
		logging.debug('Outbound lock released')
		return packet
