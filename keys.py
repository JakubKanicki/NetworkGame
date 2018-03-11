from enum import Enum

class Key(Enum):
	UP = 'w', 0
	DOWN = 's', 1
	LEFT = 'a', 2
	RIGHT = 'd', 3
	FIRE = ' ', 4

	S_UP = '8', 5
	S_DOWN = '5', 6
	S_LEFT = '4', 7
	S_RIGHT = '6', 8
	S_FIRE = ',', 9

	def __init__(self, char, id):
		self.char = char
		self.id = id

	def __eq__(self, other):
		return self.id == other

	@classmethod
	def getId(cls, char):
		for key in cls:
			if(char == key.char):
				return key.id
		return None