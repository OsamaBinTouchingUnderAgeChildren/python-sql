import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata
import mysql.connector
import datetime

run_count = 0
ADAFRUIT_IO_USERNAME = "poggersman"
ADAFRUIT_IO_KEY = "aio_sNzl93WqQXqFloB6Np3WjpLsZPRi"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

digital_output = board.get_pin('d:11:o')
analog_input = board.get_pin('a:0:i')

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="Pch3dvjm",
	database="pogchamp"
	)

mycursor = mydb.cursor()

print("Connected")

sql = "INSERT INTO poggers(verdi,tid) VALUES (%s,%s)"

try:
	digital = aio.feeds('digital')
except RequestError:
	feed = Feed(name='digital')
	digital = aio.create_feed(feed)

while True:
	print('Sending count:', run_count)
	run_count += 1
	aio.send_data('counter', run_count)
	aio.send_data('chart', analog_input.read())

	data = aio.receive(digital.key)

	print('Data: ', data.value)

	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)

	time.sleep(3)

	verdi = analog_input.read() 
	tid = datetime.datetime.now() 

	val = (verdi, tid)

	print("executing...")

	mycursor.execute(sql, val)
	mydb.commit()

	print("Done")



