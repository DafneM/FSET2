from now import *

def user_interface():

    choice = int(input("Seja bem vindo!\nO que você deseja fazer?/\n1-Alterar constantes PID\n2-Controlar por dashboard\n"))

    if(choice == 1):
        print("Defina os parâmetros desejados:")
        Kp = float(input("Kp: "))
        Ki = float(input("Ki: "))
        Kd = float(input("Kd: "))

        states['kp'] = Kp
        states['ki'] = Ki
        states['kd'] = Kd

    elif(choice == 2):
        print('Vamos começar!')