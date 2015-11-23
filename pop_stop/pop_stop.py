#Initiate serial connection to Arduino
import serial
import unirest
ser = serial.Serial('/dev/ttyUSB0', 115200)
server = "http://155.246.204.109:8000"
finish_popping_ext = "finishedPopping"

while 1 :
	if "The popcorn is now done cooking." in ser.readline():
	   print "DONE"
	   unirest.post(server + '/' + finish_popping_ext)


	