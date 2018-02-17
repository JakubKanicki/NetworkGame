import shared
import logger
from timing import Timer
from inputHandler import InputHandler
from renderer import Renderer
from map import Map
from network.networkHandler import NetworkHandler

def gameInput():
	timer.startSection('INPUT')
	inputHandler.handleInput()

def gameLogic():
	timer.startSection('LOGIC')
	packet = networkHandler.nextInbound()
	while(packet != None):
		packet.execute(map)
		packet = networkHandler.nextInbound()
	map.update()	#disable this somewhat on clients

def gameRender():
	timer.startSection('RENDER')
	renderer.render(map)


logger.init()
timer = Timer()
map = Map(96, 48)
renderer = Renderer()
inputHandler = InputHandler()
inputHandler.start()
networkHandler = NetworkHandler(False)
networkHandler.start()
while shared.running:
	gameInput()
	gameLogic()
	gameRender()
	timer.startSection('SLEEP')
	timer.sync(10)
networkHandler.stop()
logger.finish('main.log')