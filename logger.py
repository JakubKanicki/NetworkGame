import io
import time
import shared

def init():
	shared.debugStream = io.StringIO()
	debug('Debug stream started.')

def debug(val):
	if(shared.debugOutput):
		print(val)
	if(shared.debugStream != None):
		shared.debugStream.write(getTime() + '| ' + val + '\n')

def finish(fileName):
	file = open(fileName, 'w')
	file.write(shared.debugStream.getvalue())
	file.close()

def getTime():
	# return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
	return time.strftime('%H:%M:%S', time.gmtime())