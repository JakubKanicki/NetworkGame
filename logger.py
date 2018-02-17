import io
import time
import shared

def init():
	shared.debugStream = io.StringIO()
	debug('Debug stream started.')

def debug(val, isDaemon=False):
	if(shared.debugOutput):
		print(val)
	if(shared.debugStream != None):
		shared.debugStream.write(getTime() + '| ' + val + '\n')
		if(not isDaemon and shared.continuousWriting):
			finish('temp.log')	#TODO do this properly (write only new lines and not everything)

def finish(fileName):
	file = open(fileName, 'w')
	file.write(shared.debugStream.getvalue())
	file.close()

def getTime():
	# return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
	return time.strftime('%H:%M:%S', time.gmtime())