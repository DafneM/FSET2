# O init gpio tem que fazer o setup e passar o pino (nesse trabalho tem 2 saidas)
import wiringpi2 as wiringpi

def convert_gpio_to_wiring(gpio):
    if gpio == 2:
        return 8

    elif gpio == 3:
        return 9

    elif gpio == 4:
        return 7

    elif gpio == 17:
        return 0

    elif gpio == 27:
        return 2

    elif gpio == 22:
        return 3

    elif gpio == 10:
        return 12

    elif gpio == 9:
        return 13

    elif gpio == 11:
        return 14

    elif gpio == 0:
        return 30

    elif gpio == 5:
        return 21
        
    elif gpio == 6:
        return 22

    elif gpio == 13:
        return 23

    elif gpio == 19:
        return 24

    elif gpio == 26:
        return 25

    elif gpio == 14:
        return 15

    elif gpio == 15:
        return 16

    elif gpio == 18:
        return 1

    elif gpio == 23:
        return 4

    elif gpio == 24:
        return 5

    elif gpio == 25:
        return 6

    elif gpio == 8:
        return 10

    elif gpio == 7:
        return 11

    elif gpio == 1:
        return 31

    elif gpio == 12:
        return 26

    elif gpio == 16:
        return 27

    elif gpio == 20:
        return 28

    elif gpio == 21:
        return 29
        
    else:
        return -1

def init_gpio():
    wiringpi.wiringPiSetupGpio()  

    wiringpi.pinMode(23, OUTPUT)
    wiringpi.pinMode(24, OUTPUT)