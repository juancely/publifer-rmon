#!/usr/bin/python
import configparser, smbus, threading, time

ConfigFile = configparser.ConfigParser()
ConfigFile.read('config.cfg')

TSL2561 = ''
TSL2561_MIB_DEF = ''

class TSL2561(threading.Thread):

    def __init__(self, address, interval, bus):
        self._infraredLightValue = 0
        self._fullLightValue = 0
        self._visibleLightValue = 0

        self._address = address
        self._interval = interval
        self._bus = bus
        
        # TSL2561 address, 0x39(57)
        # Select control register, 0x00(00) with command register, 0x80(128)
        #       0x03(03)    Power ON mode
        self._bus.write_byte_data(self._address, 0x00 | 0x80, 0x03)
        # TSL2561 address, 0x39(57)
        # Select timing register, 0x01(01) with command register, 0x80(128)
        #       0x02(02)    Nominal integration time = 402ms
        self._bus.write_byte_data(self._address, 0x01 | 0x80, 0x02)

        time.sleep(0.5)                              # Start the execution

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                 # Start the execution 

    def getInfraredLightValue(self):
        # Output data to screen
        # print "Infrared Value :%d lux" % self._infraredLightValue
        return self._infraredLightValue  

    def getFullLightValue(self):
        # Output data to screen
        # print "Full Spectrum(IR + Visible) :%d lux" % self._fullLightValue
        # Return the data
        return self._fullLightValue

    def getVisibleLightValue(self):
        # Return the data
        return self._visibleLightValue

    def run(self):
        """ Method that runs forever """
        while True:
            # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
            # ch0 LSB, ch0 MSB
            data = self._bus.read_i2c_block_data(self._address, 0x0C | 0x80, 2)

            # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
            # ch1 LSB, ch1 MSB
            data1 = self._bus.read_i2c_block_data(self._address, 0x0E | 0x80, 2)

            # Convert the data
            ch0 = data[1] * 256 + data[0]
            ch1 = data1[1] * 256 + data1[0]

            self._fullLightValue = ch0
            self._infraredLightValue = ch1
            self._visibleLightValue = ch0 - ch1

            time.sleep(self._interval)

TSL2561 = TSL2561(
    int(ConfigFile.get('TSL2561', 'address'),16),
    int(ConfigFile.get('TSL2561', 'sampling')),
    smbus.SMBus(int(ConfigFile.get('TSL2561', 'bus')))
)

TSL2561_MIB_DEF = [
    ['tsl2561Sensor-infraredLight', 'getInfraredLightValue'],
    ['tsl2561Sensor-visibleLight', 'getVisibleLightValue'],
    ['tsl2561Sensor-fullLight', 'getFullLightValue']
]
