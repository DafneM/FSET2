from uart import *
from bme280 import *
import time
from PID import *
from now import *

def main():

    config_uart()
    # init_gpio()

    #user_interface()

    # Lendo dados da uart a cada 500ms
    while(1):
        response = read_commands() #mandando '0x23' '0xC3'
        
        if(response == '0xa1'): 
            print('Liga forno')
            states['system_state'] = 1
            transmit_data('0x16', '0xD3')

        if(response == '0xa2'): 
            print('Desliga forno')
            states['system_state'] = 0
            transmit_data('0x16', '0xD3')

        if(response == '0xa3'): 
            print('Inicia aquecimento')
            states['heating_state'] = 1
            transmit_data('0x16', '0xD5') #le temperatura de referencia
            time.sleep(1)
            reference_temp = receive_data()

            # external_temperature = sensor_temp_bme280() #le temperatura externa
            transmit_data('0x23', '0xC2') #le temperatura de referencia
            time.sleep(1)
            reference_temp = receive_data()
            # pid_atualiza_referencia(reference_temp)

            # transmit_data('0x23', '0xC1') #le temperatura interna
            # time.sleep(1)
            # intern_temp = receive_data()
            # print(f'Temperatura interna {intern_temp}')

            # pid_configura_constantes(30.0, 0.2, 400.0)
            # pid_controle(intern_temp)

            # print(sinal_de_controle)

        if(response == '0xa4'): 
            print("Cancela processo")
            states['heating_state'] = 0
            transmit_data('0x16', '0xD5') #le temperatura de referencia
            time.sleep(1)
            reference_temp = receive_data()

        if(response == '0xa5'): 
            print('Alterna modo de temperatura')

        # time.sleep(0.5)

if __name__ == '__main__':
    main()