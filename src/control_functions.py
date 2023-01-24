from uart import *
from now import *
from gpio import *
from PID import *
from sensor import *
import csv
import os

def turn_on_system():
    print('Liga forno')
    states['system_state'] = 1
    transmit_data('0x16', '0xD3')
    time.sleep(250/1000)
    turnon = receive_data()

def turn_off_system():
    print('Desliga forno')
    states['system_state'] = 0
    states['heating_state'] = 0
    states['curva_mode'] = 0

    transmit_data('0x16', '0xD3')
    time.sleep(250/1000)
    turnoff = receive_data()

    transmit_data('0x16', '0xD5')
    time.sleep(250/1000)
    led_cancel = receive_data()
    turn_off_resistor()
    turn_off_ventoinha()

    transmit_data('0x16', '0xD4') 
    time.sleep(250/1000)
    curva = receive_data()

def start_heating():
    print('Inicia aquecimento')
    states['heating_state'] = 1
    transmit_data('0x16', '0xD5') 
    time.sleep(250/1000)
    start = receive_data()

def stop_heating():
    print("Cancela processo")
    states['heating_state'] = 0

    transmit_data('0x16', '0xD5')
    time.sleep(250/1000)
    led_cancel = receive_data()
    turn_off_resistor()
    turn_off_ventoinha()

def change_temperature_mode():
    print('Alterna modo de temperatura')
    states['curva_mode'] = int(not states['curva_mode'])
    transmit_data('0x16', '0xD4')
    time.sleep(250/1000)
    temp_mode = receive_data()

def start_curva_mode(tempo):
    with open('curva_reflow.csv', 'r') as file:
        reader = csv.reader(file, delimiter=",")
        for i, line in enumerate(reader):
            if(i != 0):
                reflowtime = line[0]
                reflow_reference_temp = float(line[1])
                if(tempo == int(line[0])):
                    states['reference_temp'] = reflow_reference_temp
                    transmit_data('0x16', '0xD2')
                    pid_atualiza_referencia(states['reference_temp'])

def start_user_mode():
    #le temperatura de referencia
    transmit_data('0x23', '0xC2') 
    time.sleep(250/1000)
    uart_temp = receive_data()

    if(uart_temp != -1 and type(uart_temp) == float and uart_temp != states['internal_temp']):
        states['reference_temp'] = uart_temp
        pid_atualiza_referencia(states['reference_temp'])
        transmit_data('0x16', '0xD2')

def temperature_control(tempo):
    #le temperatura externa
    calculate_external_temp() 
    external = states['external_temp']
    transmit_data('0x16', '0xD6') 
    time.sleep(100/1000)
    external_temp = receive_data()

    if(states['curva_mode'] == 0):
        start_user_mode()

    elif(states['curva_mode'] == 1):
        start_curva_mode(tempo)

    #le temperatura interna
    transmit_data('0x23', '0xC1') 
    time.sleep(125/1000)
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
