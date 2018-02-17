import shared
import logger
from timing import Timer
from inputHandler import InputHandler
from renderer import Renderer
from map import Map

def gameInput():
	timer.startSection('INPUT')
	inputHandler.handleInput(map)

def gameLogic():
	timer.startSection('LOGIC')
	map.update()

def gameRender():
	timer.startSection('RENDER')
	renderer.render(map)


logger.init()
timer = Timer()
map = Map(96, 48)
inputHandler = InputHandler()
renderer = Renderer()
inputHandler.start()
while shared.running:
	gameInput()
	gameLogic()
	gameRender()
	timer.startSection('SLEEP')
	timer.sync(4)
logger.finish('main.log')