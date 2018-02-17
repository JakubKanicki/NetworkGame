import time
import logger

class Timer:

	def __init__(self):
		self.frameBegin = getMillis()
		self.section = None
		self.sectionStartTime = None

	def sync(self, fps):
		target = 1000 / fps
		frameTime = getMillis() - self.frameBegin
		if(frameTime > target):
			logger.debug('FRAME TIME (%d) HIGHER THAN TARGET (%d) SKIPPING SLEEP' % (frameTime, target))
			self.frameBegin = getMillis()
			return
		sleepTime = target - frameTime
		logger.debug('Frame time %d (target %d), sleeping for %d' % (frameTime, target, sleepTime))
		time.sleep(sleepTime / 1000)
		self.frameBegin = getMillis()

	def startSection(self, section):
		curTime = getMillis()
		if(self.section != None):
			sectionTime = curTime - self.sectionStartTime
			logger.debug('---END-%s-%d---' % (self.section, sectionTime))
		self.sectionStartTime = curTime
		self.section = section
		logger.debug('---START-%s---' % section)


def getMillis():
	return int(round(time.time() * 1000))