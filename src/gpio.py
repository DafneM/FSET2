# O init gpio tem que fazer o setup e passar o pino (nesse trabalho tem 2 saidas)
import RPi.GPIO as GPIO
from config import *
import time
from uart import *

resistor_pin = 0
ventoinha_pin = 0

GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

pwm_resistor = GPIO.PWM(23, 1000)

pwm_ventoinha = GPIO.PWM(24, 1000)

def init_gpio():
    global resistor_pin, ventoinha_pin, pwm

    GPIO.setmode(GPIO.BCM)
    GPIO.setmode(GPIO.BCM)

    pwm_resistor.start(0)
    pwm_ventoinha.start(0)

def turn_off_resistor():
    global resistor_pin
    pwm_resistor.ChangeDutyCycle(0)

def turn_off_ventoinha():
    global ventoinha_pin
    pwm_ventoinha.ChangeDutyCycle(0)

def clean_peripherals_communication():
    close_uart()

def activate_resistor(sinal_controle):
    global resistor_pin, ventoinha_pin

    value = int(abs(sinal_controle))

    pwm_resistor.ChangeDutyCycle(value)
    turn_off_ventoinha()

def activate_ventoinha(sinal_controle):
    global resistor_pin, ventoinha_pin

    value = int(abs(sinal_controle))

    if(sinal_controle < 0 and sinal_controle > -40): #se o sinal de controle estiver entre 0 e -40, joga pra 40%
        pwm_ventoinha.ChangeDutyCycle(40)
        turn_off_resistor()
    else:
        pwm_ventoinha.ChangeDutyCycle(value)
        turn_off_resistor()
