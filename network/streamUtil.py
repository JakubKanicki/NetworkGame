import sys

def writeInt(stream, val, byte_length):
	stream.write(val.to_bytes(byte_length, byteorder='big'))

def readInt(stream, byte_length):
	return int.from_bytes(stream.read(byte_length), byteorder='big')

def writeString(stream, val, desc_bytes=2):
	valBytes = val.encode()
	writeInt(stream, sys.getsizeof(valBytes), desc_bytes)
	stream.write(valBytes)

def readString(stream, desc_bytes=2):
	size = readInt(stream, desc_bytes)
	return stream.read(size).decode()