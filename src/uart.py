import os
import termios
import time
import struct
from cyclic_redundancy_check import *
from now import *

uart0_filestream = -1

def create_heating_message():
    message = bytes([int('6', 16), int('2', 16), int('4', 16), int('3', 16), int(str(states['heating_state']), 16)])
    return message

def create_curva_message():
    message = bytes([int('6', 16), int('2', 16), int('4', 16), int('3', 16), int(str(states['curva_mode']), 16)])
    return message

def create_status_message():
    message = bytes([int('6', 16), int('2', 16), int('4', 16), int('3', 16), int(str(states['system_state']), 16)])
    return message

def transmit_data(code, subcode):
    #endereco
    origin_address_str = '0x00'
    origin_address = bytes([int(origin_address_str, 16)])

    destination_address_str = '0x01' 
    destination_address = bytes([int(destination_address_str, 16)])

    #codigo da funcao
    code_hexa_str = code
    function_code = bytes([int(code_hexa_str, 16)])

    # DADOS
    #subcodigo
    subcode_hexa_str = subcode
    subcode = bytes([int(subcode_hexa_str, 16)])

    #matricula
    matricula = bytes([int('6', 16), int('2', 16), int('4', 16), int('3', 16)])

    if (code_hexa_str == '0x16' and subcode_hexa_str == '0xD3'): #envia estado do sistema
        message = create_status_message()
        data = bytes(subcode + message)

    elif (code_hexa_str == '0x16' and subcode_hexa_str == '0xD4'): #envia estado do sistema (manual ou curva)
        message = create_curva_message()
        data = bytes(subcode + message)

    elif (code_hexa_str == '0x16' and subcode_hexa_str == '0xD5'): #envia estado do aquecimento
        message = create_heating_message()
        data = bytes(subcode + message)

    elif (code_hexa_str == '0x16' and subcode_hexa_str == '0xD6'): #envia temperatura externa
        bytes_float_external_temp = struct.pack('f', states['external_temp'])
        data = bytes(subcode + matricula + bytes_float_external_temp)

    elif (code_hexa_str == '0x16' and subcode_hexa_str == '0xD1'): #envia sinal de controle
        bytes_representation_control_signal = struct.pack('i', int(states['control_signal']))
        data = bytes(subcode + matricula + bytes_representation_control_signal)

    elif (code_hexa_str == '0x16' and subcode_hexa_str == '0xD2'): #envia sinal de referencia
        bytes_float_reference_temp = struct.pack('f', states['reference_temp'])
        data = bytes(subcode + matricula + bytes_float_reference_temp)

    else:
        data = bytes(subcode + matricula)

    #crc
    crc = struct.pack('H', calcula_crc(destination_address + function_code + data))

    tx_buffer = bytes(destination_address + function_code + data + crc)

    if uart0_filestream != -1:
        count = os.write(uart0_filestream, tx_buffer)
        if count < 0:
            print("UART TX error")

def receive_data():
    if uart0_filestream != -1:
        rx_buffer = os.read(uart0_filestream, 255)
        rx_length = len(rx_buffer)
        if rx_length < 0:
            return -1
        elif rx_length == 0:
            return -1
        else:
            buffer_nine = rx_buffer[:9]
            
            if(len(buffer_nine) == 9):
                bytes_separados = struct.unpack("9B", buffer_nine)
                sub_bytes = bytes(rx_buffer[3:7])

                received_code = str(hex(bytes_separados[1]))
                received_subcode = str(hex(bytes_separados[2]))

                calculated_crc = struct.pack('H', calcula_crc(bytes(rx_buffer[:7])))
                crc = bytes(buffer_nine[7:10])

                if(calculated_crc == crc):
                    if(received_code == '0x23'):
                        if(received_subcode == '0xc1' or received_subcode == '0xc2'):
                            command = struct.unpack("f", sub_bytes)[0]
                            return command
                        elif(received_subcode == '0xc3'):
                            command = hex(int.from_bytes(sub_bytes, 'little'))
                            return command
                    elif(received_code == '0x16'):
                        if(received_subcode == '0xd3' or received_subcode == '0xd4' or received_subcode == '0xd5'):
                            command = hex(int.from_bytes(sub_bytes, 'little'))
                            return command
                        elif(received_subcode == '0xd6'):
                            command = hex(int(struct.unpack("f", sub_bytes)[0]))
                            return command
                
                else:
                    return -1

def read_commands():
    transmit_data('0x23', '0xC3')
    time.sleep(1)
    response = receive_data()

    return response

def close_uart():
    global uart0_filestream
    os.close(uart0_filestream)

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