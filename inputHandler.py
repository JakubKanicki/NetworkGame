from queue import Queue
from threading import Thread, Lock
import shared
import msvcrt
from network.packetKeyPressed import PacketKeyPressed
from keys import Key
import logger
import game

class InputThread(Thread):

	def __init__(self, handler):
		Thread.__init__(self)
		self.setName('INPUT_THREAD')
		self.handler = handler
		self.setDaemon(True)

	def run(self):
		self.debug('Starting thread')
		while shared.running:
			inpt = self.getInput()
			self.debug('Acquiring input lock, inpt is: ' + inpt)
			self.handler.inputLock.acquire()
			self.debug('Input lock acquired, queue size: ' + str(self.handler.inputQueue.qsize()))
			if(not self.handler.inputQueue.full()):
				self.handler.inputQueue.put(inpt)
				self.debug('Inpt added to queue')
			self.handler.inputLock.release()
			self.debug('Input lock released')
		self.debug('Exiting thread')

	def debug(self, val):
		logger.debug(self.getName() + '| ' + val, isDaemon=True)

	def getInput(self):
		while True:
			try:
				inpt = msvcrt.getch().decode("utf-8").lower()
				break
			except UnicodeDecodeError:
				pass #print("Unrecognized key")
		return inpt


class InputHandler:

	def __init__(self):
		self.inputQueue = Queue(4)
		self.inputLock = Lock()
		self.inputThread = InputThread(self)

	def start(self):
		self.inputThread.start()

	def handleInput(self):
		inptHistory = []
		logger.debug('Checking queue...')
		while not self.inputQueue.empty():
			logger.debug('Acquiring input lock...')
			self.inputLock.acquire()
			logger.debug('Input lock acquired, queue size: ' + str(self.inputQueue.qsize()))
			inpt = self.inputQueue.get()
			logger.debug('Input is: ' + inpt)
			self.inputLock.release()
			logger.debug('Input lock released')
			if(not inpt in inptHistory):
				inptHistory.append(inpt)
			process(inpt)

		logger.debug('Input handled')

def process(inpt):
	if(not shared.enableInput):
		return
	keyId = Key.getId(inpt)
	if(keyId != None):
		game.networkHandler.queueOutbound(PacketKeyPressed(keyId))
		return
	if(inpt == 'q'):
		shared.running = False
	elif(inpt == '`'):
		shared.debugRender = not shared.debugRender
	elif(inpt == '\\'):
		shared.debugOutput = not shared.debugOutput