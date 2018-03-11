from queue import Queue
from threading import Thread, Lock
import shared
import msvcrt
from network.packetKeyPressed import PacketKeyPressed
from directions import Direction
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
				pass
		return inpt


class InputHandler:

	def __init__(self):
		self.inputQueue = Queue(12)
		self.inputLock = Lock()
		self.inputThread = InputThread(self)

	def start(self):
		self.inputThread.start()

	def handleInput(self, map):
		inptHistory = []
		logger.debug('Checking queue...')
		logger.debug('Acquiring input lock...')
		self.inputLock.acquire()					# have to lock input for the duration of the loop to prevent more than queue size inputs per frame
		logger.debug('Input lock acquired')
		while not self.inputQueue.empty():
			logger.debug('Input queue size: ' + str(self.inputQueue.qsize()))
			inpt = self.inputQueue.get()
			logger.debug('Input is: ' + inpt)
			if(not inpt in inptHistory):
				inptHistory.append(inpt)
			process(inpt, map)
		self.inputLock.release()
		logger.debug('Input lock released')
		logger.debug('Input handled')


def process(inpt, map):
	if(not shared.enableInput):
		return
	keyId = Key.getId(inpt)
	if(keyId != None):
		if(shared.isNetworked):
			game.networkHandler.queueOutbound(PacketKeyPressed(keyId))
		else:
			processNetworked(map, keyId)
		return
	if(inpt == 'q'):
		shared.running = False
	elif(inpt == '`'):
		shared.debugRender = not shared.debugRender
	elif(inpt == '\\'):
		shared.debugOutput = not shared.debugOutput

def processNetworked(map, keyId):
	if (keyId == Key.UP):
		map.players[0].move(map, Direction.UP)
	elif (keyId == Key.DOWN):
		map.players[0].move(map, Direction.DOWN)
	elif (keyId == Key.LEFT):
		map.players[0].move(map, Direction.LEFT)
	elif (keyId == Key.RIGHT):
		map.players[0].move(map, Direction.RIGHT)
	elif (keyId == Key.FIRE):
		map.spawnProjectile(map.players[0].x, map.players[0].y, 0, map.players[0].direction)

	elif (keyId == Key.S_UP):
		map.players[1].move(map, Direction.UP)
	elif (keyId == Key.S_DOWN):
		map.players[1].move(map, Direction.DOWN)
	elif (keyId == Key.S_LEFT):
		map.players[1].move(map, Direction.LEFT)
	elif (keyId == Key.S_RIGHT):
		map.players[1].move(map, Direction.RIGHT)
	elif (keyId == Key.S_FIRE):
		map.spawnProjectile(map.players[1].x, map.players[1].y, 0, map.players[1].direction)