import csv
import datetime
from now import *
import os

def write_csv():
    ventoinha_state = 0
    resistor_state = 0

    date_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    if states['control_signal'] > 0:
        resistor_state = int(states['control_signal'])
    elif states['control_signal'] < 0:
        ventoinha_state = abs(int(states['control_signal']))

    internal = states['internal_temp']
    external = states['external_temp']

    writer = open('states.csv', 'a')
    writer.write(f'{date_time}, Temperatura interna: {round(internal, 2)}, Temperatura externa: {round(external, 2)}, Valor de acionamento do resistor: {resistor_state}% , Valor de acionamento da ventoinha: {ventoinha_state}% \n\n')
    writer.close()