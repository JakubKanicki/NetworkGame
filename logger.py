import io
import time
import shared


def init():		# TODO probably replace this with the built-in logging module
	shared.debugStream = io.StringIO()
	debug('Debug stream started.')

def debug(val, isDaemon=False):
	if(shared.debugOutput):
		print(val)
	if(shared.debugStream != None):
		line = getTime() + '| ' + val + '\n'
		shared.debugStream.write(line)
		if(shared.continuousWriting):
			temp = 'daemon.log' if isDaemon else 'temp.log'
			if(not shared.isClient):
				temp = 'server_' + temp
			if(shared.debugStreamStarted):
				append(temp, line)
			else:
				finish(temp)
				shared.debugStreamStarted = True

def append(fileName, line):
	file = open(fileName, 'a+')
	file.write(line)
	file.close()

def finish(fileName):
	file = open(fileName, 'w+')
	file.write(shared.debugStream.getvalue())
	file.close()

def getTime():
	# return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
	return time.strftime('%H:%M:%S', time.gmtime())