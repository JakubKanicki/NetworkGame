from queue import Queue
from threading import Thread, Lock
import shared
import msvcrt
from directions import Direction


class InputThread(Thread):

	def __init__(self, handler):
		Thread.__init__(self)
		self.setName('INPUT_THREAD')
		self.handler = handler

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
		if(shared.debugOutput):
			print(self.getName() + '| ' + val)

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

	def debug(self, val):
		if(shared.debugOutput):
			print(val)

	def handleInput(self, map):
		inptHistory = []
		self.debug('Checking queue...')
		while not self.inputQueue.empty():
			self.debug('Acquiring input lock...')
			self.inputLock.acquire()
			self.debug('Input lock acquired, queue size: ' + str(self.inputQueue.qsize()))
			inpt = self.inputQueue.get()
			self.debug('Input is: ' + inpt)
			self.inputLock.release()
			self.debug('Input lock released')
			if(not inpt in inptHistory):
				inptHistory.append(inpt)
				self.process(map, inpt)
		self.debug('Input handled')

	def process(self, map, inpt):
		if(not shared.enableInput):
			return
		if(inpt == 'q'):
			shared.running = False
		elif(inpt == 'w'):
			map.player.move(map, Direction.UP)
		elif(inpt == 's'):
			map.player.move(map, Direction.DOWN)
		elif(inpt == 'a'):
			map.player.move(map, Direction.LEFT)
		elif(inpt == 'd'):
			map.player.move(map, Direction.RIGHT)
		elif(inpt == ' '):
			map.spawnProjectile(map.player.x, map.player.y, 0, map.player.direction)
		elif(inpt == '`'):
			shared.debugRender = not shared.debugRender
		elif(inpt == '\\'):
			shared.debugOutput = not shared.debugOutput