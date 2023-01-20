def user_interface():


    choice = float(input("O que vocẽ deseja alterar/\n1-Temperatura de referencia\n2-Constantes PID\n"))

    if(choice == 1):
        reference_temp = float(input("Defina a temperatura de referência desejada: "))
    
    elif(choice == 2):
        print("Defina os parâmetros desejados:")
        Kp = float(input("Kp: "))
        Ki = float(input("Ki: "))
        Kd = float(input("Kd: "))