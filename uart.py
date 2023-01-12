import os
import termios
import time
import struct
from filez import *

uart0_filestream = -1

def create_buffer(address, code, subcode):
    ...

def transmit_data():
    #endereco
    origin_address_str = '0x00'
    origin_address = bytes([int(origin_address_str, 16)])

    destination_address_str = '0x01' 
    destination_address = bytes([int(destination_address_str, 16)])

    #codigo da funcao
    code_hexa_str = '0x23'
    function_code = bytes([int(code_hexa_str, 16)])

    # DADOS
    #subcodigo
    subcode_hexa_str = '0xC3'
    subcode = bytes([int(subcode_hexa_str, 16)])

    #matricula
    matricula = bytes([int('6', 16), int('2', 16), int('4', 16), int('3', 16)])

    data = bytes(subcode + matricula)

    #crc
    crc = struct.pack('H', calcula_crc(destination_address + function_code + data))

    tx_buffer = bytes(destination_address + function_code + data + crc)

    if uart0_filestream != -1:
        print("Escrevendo caracteres na UART ...")
        count = os.write(uart0_filestream, tx_buffer)
        if count < 0:
            print("UART TX error")
        else:
            print("Escrito.")

def receive_data():
    ...

def read_commands():
    transmit_data()
    receive_data()

def config_uart():
    global uart0_filestream
    uart0_filestream = os.open("/dev/serial0", os.O_RDWR | os.O_NOCTTY | os.O_NDELAY)
    if uart0_filestream == -1:
        print("Erro - Não foi possível iniciar a UART.")
    else:
        print("UART inicializada!")

    options = termios.tcgetattr(uart0_filestream)
    options[2] = termios.B9600 | termios.CS8 | termios.CLOCAL | termios.CREAD 
    options[0] = termios.IGNPAR 
    options[1] = 0
    options[3] = 0 
    termios.tcflush(uart0_filestream, termios.TCIFLUSH) 
    termios.tcsetattr(uart0_filestream, termios.TCSANOW, options)