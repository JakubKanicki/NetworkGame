import shared
import msvcrt
import sys
from directions import Direction

def handleInput(map):
	if(not shared.enableInput):
		return

	while True:
		try:
			inpt = msvcrt.getch().decode("utf-8").lower()
			break
		except UnicodeDecodeError:
			pass #print("Unrecognized key")

	if(inpt == 'q'):
		shared.running = False
		print("Shutting down...")
	elif(inpt == 'w'):
		map.movePlayer(Direction.UP)
	elif(inpt == 's'):
		map.movePlayer(Direction.DOWN)
	elif(inpt == 'a'):
		map.movePlayer(Direction.LEFT)
	elif(inpt == 'd'):
		map.movePlayer(Direction.RIGHT)
	elif(inpt == ' '):
		map.spawnProjectile(map.player.x, map.player.y, 0, map.player.direction)
	elif(inpt == '`'):
		shared.debugRender = not shared.debugRender
		