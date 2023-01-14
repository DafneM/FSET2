import time
import smbus2
import bme280
# RPi_I2C_driver can be found here: https://gist.github.com/DenisFromHR/cc863375a6e19dce359d

def calculate_external_temp():
    try:
        while(1):
            sensor_temp_bme280()
            time.sleep(1)
    
    except KeyboardInterrupt:
        print('finalizando...')

def sensor_temp_bme280():
    
    # sensor bme280
    port = 1
    sensor_address = 0x76
    bus = smbus2.SMBus(port)

    params = bme280.load_calibration_params(bus, sensor_address)

    data = bme280.sample(bus, sensor_address, params)
    external_temperature = data.temperature

    return external_temperature
  
