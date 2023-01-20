import csv
import datetime
from now import *

def write_csv():
    date_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    data = [{'Data e hora':date_time}, {'Temperatura interna': states['internal_temp']}, {'Temperatura externa': states['external_temp']}, {'Temperatura definida': states['user_temp']}, {'Valor de acionamento': states['activation_value']}]

    with open('states.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def write_csv2():
    data = [['Name', 'Age'],
        ['Bob', 25],
        ['Alice', 22],
        ['Charlie', 27]]

    with open('states.csv', 'w') as file:
        for row in data:
            file.write(','.join(str(i) for i in row) + '\n')
