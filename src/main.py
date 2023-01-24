from uart import *
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
from control_functions import *

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
    clean_peripherals_communication()

    turn_off_resistor()
    turn_off_ventoinha()

    run_thread = False
    os._exit(0)

def threaded_function(): 
    while (run_thread):
        write_csv()
        
        time.sleep(1) 

def main():
    signal.signal(signal.SIGINT, signal_handler)

    config_uart()
    init_gpio()
    init_system()

    user_interface()

    thread = Thread(target = threaded_function, args = ()) 
    thread.start() 

    while(1):
        global tempo

        response = read_commands()
        
        if(response == '0xa1'): 
            turn_on_system()
            tempo = 0

        if(response == '0xa2'): 
            turn_off_system()

        if(response == '0xa3'): 
            if(states['system_state'] == 1):
                start_heating()
                
        if(response == '0xa4'): 
            stop = 0
            stop_heating()

        if(response == '0xa5'): 
            change_temperature_mode()
        
        if(states['system_state'] == 1 and states['heating_state'] == 1):
            temperature_control(tempo)

        if(states['system_state'] == 1):
            tempo+=1
    
    thread.join()

if __name__ == '__main__':
    main()
