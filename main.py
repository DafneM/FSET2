from uart import *
from sensor import *
import time
from PID import *
from now import *
from gpio import *
from manipulate_csv import *
import signal
import sys
from threading import Thread 
import os
import csv
from ui import *

run_thread = True
tempo = 0

def init_system():
    states['system_state'] = 0
    transmit_data('0x16', '0xD3')
    time.sleep(250/1000)
    turnoff = receive_data()

    states['heating_state'] = 0
    transmit_data('0x16', '0xD5') 
    time.sleep(250/1000)
    stop = receive_data()

    states['curva_mode'] = 0
    transmit_data('0x16', '0xD4') 
    time.sleep(250/1000)
    curva = receive_data()

def signal_handler(sig, frame):
    # Encerra comunicações com perifericos
    clean_peripherals_communication() #!!!! IMPLEMENTAR

    # Desliga atuadores
    turn_off_resistor()
    turn_off_ventoinha()

    run_thread = False
    sys.exit(0)

def threaded_function(): 
    while (run_thread):
        write_csv2()
        
        time.sleep(1) 

def main():
    signal.signal(signal.SIGINT, signal_handler)

    config_uart()
    init_gpio()
    init_system()

    user_interface()

    thread = Thread(target = threaded_function, args = ()) 
    thread.start() 

    # Lendo dados da uart a cada 500ms
    while(1):
        global tempo

        response = read_commands() #mandando '0x23' '0xC3'

        # LIGA FORNO
        if(response == '0xa1'): 
            print('Liga forno')
            states['system_state'] = 1
            transmit_data('0x16', '0xD3')
            time.sleep(250/1000)
            turnon = receive_data()
            tempo = 0

        # DESLIGA FORNO
        if(response == '0xa2'): 
            print('Desliga forno')
            states['system_state'] = 0
            transmit_data('0x16', '0xD3')
            time.sleep(250/1000)
            turnoff = receive_data()

        # INICIAR AQUECIMENTO
        if(response == '0xa3'): 
            if(states['system_state'] == 1):
                print('Inicia aquecimento')
                states['heating_state'] = 1
                transmit_data('0x16', '0xD5') 
                time.sleep(250/1000)
                start = receive_data()
                
        # CANCELA PROCESSO
        if(response == '0xa4'): 
            print("Cancela processo")
            states['heating_state'] = 0
            stop = 0

            #Envia comando apagar led do cancela processo
            transmit_data('0x16', '0xD5')
            time.sleep(250/1000)
            led_cancel = receive_data()
            turn_off_resistor()
            turn_off_ventoinha()

        # TROCA MODO DE TEMPERATURA
        if(response == '0xa5'): 
            print('Alterna modo de temperatura')
            states['curva_mode'] = int(not states['curva_mode'])
            transmit_data('0x16', '0xD4')
            time.sleep(250/1000)
            temp_mode = receive_data()
        
        # CONTROLE DE TEMPERATURA
        if(states['system_state'] == 1 and states['heating_state'] == 1):
            #le temperatura externa
            calculate_external_temp() 
            external = states['external_temp']
            transmit_data('0x16', '0xD6') 
            time.sleep(250/1000)
            external_temp = receive_data()

            if(states['curva_mode'] == 0):
                print('entrei no 2')
                #le temperatura de referencia
                transmit_data('0x23', '0xC2') 
                time.sleep(250/1000)
                uart_temp = receive_data()

                if(uart_temp != -1 and type(uart_temp) == float and uart_temp != states['internal_temp']):
                    states['reference_temp'] = uart_temp
                    x = states['reference_temp']
                    pid_atualiza_referencia(states['reference_temp'])
                    transmit_data('0x16', '0xD2')

            elif(states['curva_mode'] == 1):
                print('Entrei no modo curva')
                with open('curva_reflow.csv', 'r') as file:
                    reader = csv.reader(file, delimiter=",")
                    print(f'to no tempo {tempo}')
                    for i, line in enumerate(reader):
                        if(i != 0):
                            reflowtime = line[0]
                            reflow_reference_temp = float(line[1])
                            if(tempo == int(line[0])):
                                print(f'entrei no tempo {tempo}')
                                states['reference_temp'] = reflow_reference_temp
                                transmit_data('0x16', '0xD2')
                                pid_atualiza_referencia(states['reference_temp'])

            #le temperatura interna
            transmit_data('0x23', '0xC1') 
            time.sleep(250/1000)
            internal_temp = receive_data()
            if(internal_temp != -1 and type(internal_temp) == float and internal_temp != states['reference_temp']):
                states['internal_temp'] = internal_temp

            pid_configura_constantes(states['kp'], states['ki'], states['kd'])
            states['control_signal'] = pid_controle(states['internal_temp'])

            if(states['control_signal'] < 0):
                activate_ventoinha(states['control_signal'])

            elif(states['control_signal'] > 0):
                activate_resistor(states['control_signal'])

            transmit_data('0x16', '0xD1')

        if(states['system_state'] == 1):
            tempo+=1

if __name__ == '__main__':
    main()
