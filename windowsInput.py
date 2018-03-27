import msvcrt

def getch():
	try:
		return msvcrt.getch().decode("utf-8").lower()
	except UnicodeDecodeError:
		return None