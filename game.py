import sys
import shared
import logger
from timing import Timer
from inputHandler import InputHandler
from renderer import Renderer
from map import Map
from network.networkHandler import NetworkHandler


def gameInput():
	timer.startSection('INPUT')
	inputHandler.handleInput(map)

def gameLogic():
	if(shared.isNetworked):
		timer.startSection('NETWORK_INBOUND_LOGIC')
		packet = networkHandler.nextInbound()
		while(packet != None):
			packet.execute(map)
			packet = networkHandler.nextInbound()
	timer.startSection('LOGIC')
	map.update()		# disable this somewhat on clients

def gameRender():
	timer.startSection('RENDER')
	renderer.render(map)


logger.init()
for arg in sys.argv:
	if(arg.lower() == 'server'):
		shared.isClient = False
		shared.isNetworked = True
		logger.debug('Running server')
	elif(arg.lower() == 'client'):
		shared.isClient = True
		shared.isNetworked = True
		logger.debug('Running client')
	elif (len(arg) > 3 and arg.lower()[:3] == 'ip='):
		shared.host = arg.lower()[3:]
		logger.debug('IP: ' + str(shared.host))
	elif (len(arg) > 5 and arg.lower()[:5] == 'port='):
		shared.port = int(arg.lower()[5:])
		logger.debug('Port: ' + str(shared.port))

timer = Timer()
map = Map(96, 48)
renderer = Renderer()
inputHandler = InputHandler()
inputHandler.start()
if(shared.isNetworked):
	networkHandler = NetworkHandler()
	networkHandler.start()
while shared.running:
	gameLogic()
	gameRender()
	gameInput()
	timer.startSection('SLEEP')
	timer.sync(10)
if(shared.isNetworked):
	networkHandler.stop()
logger.finish('main.log' if shared.isClient else 'server.log')