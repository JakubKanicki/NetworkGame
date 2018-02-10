import time
import shared
from inputHandler import InputHandler
from renderer import Renderer
from map import Map

def gameInput():
	debug('-INPUT-')
	inputHandler.handleInput(map)
	
def gameLogic():
	debug('-LOGIC-')
	map.update()

def gameRender():
	debug('-RENDER-')
	renderer.render(map)

def debug(val):
	if(shared.debugOutput):
		print(val)

map = Map(96, 48)
inputHandler = InputHandler()
renderer = Renderer()
inputHandler.start()
while shared.running:
	gameInput()
	gameLogic()
	gameRender()
	time.sleep(0.05)