#!/usr/bin/python
import configparser, smbus, threading, time

ConfigFile = configparser.ConfigParser()
ConfigFile.read('config.cfg')

class TMP75(threading.Thread):

	def __init__(self, address, interval, bus):
		self._cTempValue = 0
		self._fTempValue = 0

		self._address = address
		self._interval = interval
		self._bus = bus

		data = [0x60A0]
		self._bus.write_i2c_block_data(self._address, 0x01, data)

		time.sleep(0.5)

		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True   
		thread.start() 

	def getcTempValue(self):
		return self._cTempValue * 10

	def run(self):
		while True:
			data = self._bus.read_i2c_block_data(self._address, 0x00, 2)

			# Convert the data
			temp =(data[0] * 256 + data[1]) / 16
			if temp > 2047 :
				temp -= 4096
			cTemp = temp * 0.0625
			fTemp = cTemp * 1.8 + 32

			self._cTempValue = cTemp
			self._fTempValue = fTemp

			# Output data to screen
			# print ("Temperature in Celsius is : %.2f C" %cTemp)
			# print ("Temperature in Fahrenheit is : %.2f F" %fTemp)
			time.sleep(self._interval)

TMP75 = TMP75(
    int(ConfigFile.get('TMP75', 'address'),16),
    int(ConfigFile.get('TMP75', 'sampling')),
    smbus.SMBus(int(ConfigFile.get('TMP75', 'bus')))
)

TMP75_MIB_DEF = [
    ['tmp75Sensor-value', 'getcTempValue']
]
