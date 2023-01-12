from uart import *
import time

def main():

    config_uart()

    # Lendo dados da uart a cada 500ms
    while(1):
        read_commands() #mandando '0x23' '0xC3'
        
        # if('0Xa1'): liga led
        # if('0Xa1'): desliga led

        # controle_temperatura

        time.sleep(0.5)

if __name__ == '__main__':
    main()