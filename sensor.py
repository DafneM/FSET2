import time
import smbus2
import bme280
from config import *
from now import *
import Adafruit_BME280

def calculate_external_temp():
    
    port = configs['bme_port']
    BME280_I2C_ADDR = configs['bme_addr']
    bus = smbus2.SMBus(port)

    params = bme280.load_calibration_params(bus,  BME280_I2C_ADDR)

    try:
        # while(1):
        data = bme280.sample(bus,  BME280_I2C_ADDR, params)
        print(f'data {data.temperature}')
        states['external_temp'] = float(data.temperature)
        a = states['external_temp']
        print(f'states {a}')
        # time.sleep(1)
    
    except KeyboardInterrupt:
        print('finalizando...')