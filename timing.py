import time
import logging


class Timer:

	def __init__(self):
		self.frameBegin = getMillis()
		self.section = None
		self.sectionStartTime = None

	def sync(self, fps):
		target = 1000 / fps
		frameTime = getMillis() - self.frameBegin
		if(frameTime > target):
			logging.warning('Frame time (%d) higher than target (%d) skipping sleep' % (frameTime, target))
			self.frameBegin = getMillis()
			return
		sleepTime = target - frameTime
		logging.debug('Frame time %d (target %d), sleeping for %d' % (frameTime, target, sleepTime))
		time.sleep(sleepTime / 1000)
		self.frameBegin = getMillis()

	def startSection(self, section):
		curTime = getMillis()
		if(self.section != None):
			sectionTime = curTime - self.sectionStartTime
			logging.debug('---END-%s-%d---' % (self.section, sectionTime))
		self.sectionStartTime = curTime
		self.section = section
		logging.debug('---START-%s---' % section)


def getMillis():
	return int(round(time.time() * 1000))