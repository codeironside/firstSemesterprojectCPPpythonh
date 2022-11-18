import math

import pygame
import os
import math

from pygame import mixer
import serial
import time
import re

arduino = serial.Serial('COM5', 9600)
screen_height = 1080
screen_width = 1920
display_size = (screen_width, screen_height)


def sensor_value():

    b = arduino.readline()
    string_n = b.decode()
    string = string_n.rstrip()
    all_sensor = re.split(',', string)
    left_sensor = all_sensor[1]
    right_sensor = all_sensor[0]
    # print(left_sensor, right_sensor)

    print(left_sensor, right_sensor)
    #return left_sensor, right_sensor