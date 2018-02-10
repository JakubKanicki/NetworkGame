import shared
import inputHandler
from renderer import Renderer
from map import Map


def gameInput():
	print('-INPUT-')
	inputHandler.handleInput(map)
	
def gameLogic():
	print('-LOGIC-')
	map.update()

def gameRender():
	print('-RENDER-')
	renderer.render(map)


map = Map(92, 48)
renderer = Renderer()
while shared.running:
	gameInput()
	gameLogic()
	gameRender()