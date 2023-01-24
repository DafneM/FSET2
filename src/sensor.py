import time
import smbus2
import bme280
from config import *
from now import *

def calculate_external_temp():
    
    port = configs['bme_port']
    BME280_I2C_ADDR = configs['bme_addr']
    bus = smbus2.SMBus(port)

    params = bme280.load_calibration_params(bus,  BME280_I2C_ADDR)

    try:
        data = bme280.sample(bus,  BME280_I2C_ADDR, params)
        states['external_temp'] = float(data.temperature)
        a = states['external_temp']
    
    except KeyboardInterrupt:
        print('finalizando...')