#!/usr/bin/python
import configparser, smbus, threading, time

ConfigFile = configparser.ConfigParser()
ConfigFile.read('config.cfg')

class ADS7828(threading.Thread):

    def __init__(self, address, interval, bus):
        self._adsValue = 0

        self._address = address
        self._interval = interval
        self._bus = bus

        # Config Register
        self.__ADS7828_CONFIG_SD_DIFFERENTIAL      = 0b00000000
        self.__ADS7828_CONFIG_SD_SINGLE            = 0b10000000
        self.__ADS7828_CONFIG_CS_CH0               = 0b00000000
        self.__ADS7828_CONFIG_CS_CH2               = 0b00010000
        self.__ADS7828_CONFIG_CS_CH4               = 0b00100000
        self.__ADS7828_CONFIG_CS_CH6               = 0b00110000
        self.__ADS7828_CONFIG_CS_CH1               = 0b01000000
        self.__ADS7828_CONFIG_CS_CH3               = 0b01010000
        self.__ADS7828_CONFIG_CS_CH5               = 0b01100000
        self.__ADS7828_CONFIG_CS_CH7               = 0b01110000
        self.__ADS7828_CONFIG_PD_OFF               = 0b00000000
        self.__ADS7828_CONFIG_PD_REFOFF_ADON       = 0b00000100
        self.__ADS7828_CONFIG_PD_REFON_ADOFF       = 0b00001000
        self.__ADS7828_CONFIG_PD_REFON_ADON        = 0b00001100

        time.sleep(0.5)

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                 # Start the execution 

    def readChannel(self, ch):
        config = 0
        config |= self.__ADS7828_CONFIG_SD_SINGLE
        config |= self.__ADS7828_CONFIG_PD_REFOFF_ADON

        if ch == 0:
                config |= self.__ADS7828_CONFIG_CS_CH0
        elif ch == 1:
                config |= self.__ADS7828_CONFIG_CS_CH1
        elif ch == 2:
                config |= self.__ADS7828_CONFIG_CS_CH2
        elif ch == 3:
                config |= self.__ADS7828_CONFIG_CS_CH3
        elif ch == 4:
                config |= self.__ADS7828_CONFIG_CS_CH4
        elif ch == 5:
                config |= self.__ADS7828_CONFIG_CS_CH5
        elif ch == 6:
                config |= self.__ADS7828_CONFIG_CS_CH6
        elif ch == 7:
                config |= self.__ADS7828_CONFIG_CS_CH7

        data = self._bus.read_i2c_block_data(self._address, config, 2)
        return ((data[0] << 8) + data[1])

    def getAdsValue(self):
        # print(self._adsValue)
        ads = self._adsValue * 10000
        # print(ads)
        return ads
        
    def run(self):
        
        while True:

            h = self.readChannel(6)
            self._adsValue = (h * 5.0) / 4095

            time.sleep(self._interval)

ADS7828 = ADS7828(
    int(ConfigFile.get('ADS7828', 'address'),16),
    int(ConfigFile.get('ADS7828', 'sampling')),
    smbus.SMBus(int(ConfigFile.get('ADS7828', 'bus')))
)

ADS7828_MIB_DEF = [
    ['ads7828Sensor-value', 'getAdsValue']
]
