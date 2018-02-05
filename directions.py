
class Direction():
	UP = 0;
	DOWN = 1;
	LEFT = 2;
	RIGHT = 3;

def getVec(direction):
	if(direction == Direction.UP):
		return (0, -1)
	elif(direction == Direction.DOWN):
		return (0, 1)
	elif(direction == Direction.LEFT):
		return (-1, 0)
	elif(direction == Direction.RIGHT):
		return (1, 0)