import sys
import os
import shared
import logging
import time
from timing import Timer
from inputHandler import InputHandler
from renderer import Renderer
from map import Map


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


# if(os.path.exists(log)):
# 	os.remove(log)
logging.basicConfig(filename=str(time.time()) + '.log',
					format='%(levelname)s|%(msecs)d|%(threadName)s|%(module)s|%(message)s',
					level=logging.INFO)

for arg in sys.argv:
	if(arg.lower() == 'server'):
		from network.server import NetworkHandler
		shared.isClient = False
		shared.isNetworked = True
		logging.info('Running server')
	elif(arg.lower() == 'client'):
		from network.client import NetworkHandler
		shared.isClient = True
		shared.isNetworked = True
		logging.info('Running client')
	elif (len(arg) > 3 and arg.lower()[:3] == 'ip='):
		shared.host = arg.lower()[3:]
		logging.info('IP: ' + str(shared.host))
	elif (len(arg) > 5 and arg.lower()[:5] == 'port='):
		shared.port = int(arg.lower()[5:])
		logging.info('Port: ' + str(shared.port))

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