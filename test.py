import serial
import time
import re

arduino = serial.Serial('COM5', 9600)


def arduino_read():
    while True:
        b = arduino.readline()
        string_n = b.decode()
        string = string_n.rstrip()
        all_sensor = re.split(',', string)
        left_sensor = all_sensor[1]
        right_sensor = all_sensor[0]
        return right_sensor, left_sensor


while True:
    print(arduino_read())
