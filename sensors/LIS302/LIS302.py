#!/usr/bin/python
import configparser, smbus, threading, time

ConfigFile = configparser.ConfigParser()
ConfigFile.read('config.cfg')

LIS302 = ''
LIS302_MIB_DEF = ''

class LIS302(threading.Thread):
	def __init__(self, address, interval, bus):

		self._address = address
		self._interval = interval
		self._bus = bus

		self._CTRL_REG1 			= 	0x20
		self._CTRL_REG2 			= 	0x21
		self._CTRL_REG3 			= 	0x22

		self._HP_FILTER_RST       = 	0x23
		self._STATUS_REG          =	0x27

		self._FF_WU_CFG_1 		= 	0x30
		self._FF_WU_THS_1      	= 	0x32
		self._FF_WU_DURATION_1 	= 	0x33
		self._FF_WU_SRC_1      	= 	0x31

		self._STATUS = 0
		self._OK = True 

		data = [0x47]
		self._bus.write_i2c_block_data(self._address, self._CTRL_REG1, data)
		data = [0x00]
		self._bus.write_i2c_block_data(self._address, self._CTRL_REG2, data)
		data = [0x08]
		self._bus.write_i2c_block_data(self._address, self._CTRL_REG3, data)
		data = [0x0A]
		self._bus.write_i2c_block_data(self._address, self._FF_WU_THS_1, data)
		data = [0x00]
		self._bus.write_i2c_block_data(self._address, self._FF_WU_DURATION_1, data)
		data = [0x4A]
		self._bus.write_i2c_block_data(self._address, self._FF_WU_CFG_1, data)

		time.sleep(0.5) 

		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True                            # Daemonize thread
		thread.start() 

	def getStatus(self):
		return self._STATUS

	def run(self):

		while True:

			if(self._OK == True):
				# print('Status: OK')
				zz = self._bus.read_byte_data(self._address,self._FF_WU_SRC_1)
				h = hex(zz)

				if(h != hex(0x05)):
					print('Choc Detected')

					time.sleep(1)

					zz = self._bus.read_byte_data(self._address,self._FF_WU_SRC_1)
					h = hex(zz)

					if(h == hex(0x05)):
						self._OK = True
						self._STATUS = 0
					else:
						self._OK = False
						self._STATUS = 1
				else:
					self._OK = True
					self._STATUS = 0
			else:
				print('Status: DOWN')

				time.sleep(1)

				zz = self._bus.read_byte_data(self._address,self._FF_WU_SRC_1)
				h = hex(zz)

				if(h == hex(0x05)):
					self._OK = True
					self._STATUS = 0
				else:
					self._OK = False
					self._STATUS = 2

			time.sleep(self._interval)

LIS302 = LIS302(
    int(ConfigFile.get('LIS302', 'address'),16),
    int(ConfigFile.get('LIS302', 'sampling')),
    smbus.SMBus(int(ConfigFile.get('LIS302', 'bus')))
)

LIS302_MIB_DEF = [
    ['lis302Sensor-value', 'getStatus']
]
