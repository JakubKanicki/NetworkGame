import time
import shared
import logger
from inputHandler import InputHandler
from renderer import Renderer
from map import Map

def gameInput():
	logger.debug('-INPUT-')
	inputHandler.handleInput(map)
	
def gameLogic():
	logger.debug('-LOGIC-')
	map.update()

def gameRender():
	logger.debug('-RENDER-')
	renderer.render(map)

logger.init()
map = Map(96, 48)
inputHandler = InputHandler()
renderer = Renderer()
inputHandler.start()
while shared.running:
	gameInput()
	gameLogic()
	gameRender()
	logger.debug('-SLEEP-')
	time.sleep(0.1)
logger.finish('main.log')