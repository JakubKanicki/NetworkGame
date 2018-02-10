# https://www.tutorialspoint.com/python3/python_multithreading.htm
import threading
import time
import queue
import random


class WorkThread(threading.Thread):

	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		print('Thread created: ' + self.name)

	def run(self):
		self.tPrint('Thread started')

		while not exitFlag:
			qLock.acquire()
			if(not workQueue.empty()):
				self.tPrint('Lock acquired queue size is %d ' % workQueue.qsize())
				item = workQueue.get()
				qLock.release()
				self.tPrint('Lock released, sleeping for %d seconds ' % item)
				time.sleep(item)
			else:
				qLock.release()
				self.tPrint('...')
				time.sleep(0.5)

		self.tPrint('Thread over')

	def tPrint(self, val):
		print('%s | %s: ' % (getTime(), self.getName()) + val)


def getTime():
	# return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
	return time.strftime('%H:%M:%S', time.gmtime())


threadNames = ['Uno', 'Duo', 'Trio', 'NVidia Quadro', 'Punto']
workQueue = queue.Queue()
qLock = threading.Lock()
threads = []
exitFlag = False

print('MAIN: Program start')

for threadName in threadNames:
	threads.append(WorkThread(threadName))
print('MAIN: Threads created')

for thread in threads:
	thread.start()
print('MAIN: Threads started')

for i in range(24):
	qLock.acquire()
	workQueue.put(random.randrange(4)+1)
	qLock.release()
	time.sleep(0.2)
print('MAIN: Work queue filled')

while(not workQueue.empty()):
	time.sleep(0.5)
exitFlag = True
print('MAIN: Work queue empty, set exit flag')

for thread in threads:
	thread.join()
print('MAIN: Threads joined, exiting main thread...')