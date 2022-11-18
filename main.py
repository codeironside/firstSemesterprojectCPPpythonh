import math

import pygame
import os
import math

from pygame import mixer
import serial
import time
import re
from time import 

screen_height = 1080
screen_width = 1920
display_size = (screen_width, screen_height)

arduino = serial.Serial('COM40', 9600,timeout=1)



left_sensor = 0
right_sensor = 0
all_sensor = ["0","0"]



def sensor_value():
    b = arduino.readline()
    string_n = b.decode()
    string = string_n.rstrip()
    all_sensor = re.split(',', string)

    left_sensor = all_sensor[1]
    right_sensor = all_sensor[0]


    return int(left_sensor), int(right_sensor) 


pygame.init()
clock = pygame.time.Clock()
FPS = 1000
GRAVITY = 0.85
screen = pygame.display.set_mode(display_size)

backgrounds = []
for background in range(len(os.listdir('assets/backgrounds'))):
    backgrounds.append(background)

bg = pygame.image.load(f'assets/backgrounds/{backgrounds[6]}.jpg').convert()
bg_width = bg.get_width()
bg_height = bg.get_height()

# jet = pygame.image.load(f'assets/jets/player/jet00.png').convert_alpha()
# jet_width = bg.get_width()
# jet_height = bg.get_height()
# scale = 0.08
# jet = pygame.transform.scale(jet, (int(jet_height*scale),int(jet_height*scale)))


### define game variables
tiles = math.ceil(screen_width / bg_width) + 1
tile_height = math.ceil(screen_height / bg_height) + 1
scroll = 0

### sound variables
mixer.init()
mixer.music.load('assets/sound/jetidle.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

### initializers
moving_left = False
moving_right = False


#### jet object ############

class Jet(pygame.sprite.Sprite):
    def __init__(self, jetType, x, y, lives, ammo, speed, direction, scale):
        super().__init__()
        self.jetType = jetType
        self.lives = lives
        self.ammo = ammo
        self.speed = speed
        self.jetType = jetType
        self.direction = direction
        self.scale = scale
        self.alive = True
        self.flip = False

        img = pygame.image.load(f'assets/jets/{self.jetType}/jet00.png').convert_alpha()
        self.image = pygame.transform.scale(img,
                                            (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        y = screen_height - (self.height * self.scale) - 100
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.direction = -1

        if moving_right:
            dx = self.speed
            self.direction = 1

        if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
            self.direction *= -1
            dx = self.direction * self.speed

        self.rect.x += dx
        self.rect.y += dy
        # print(dx, dy)

    # print(right_sensor, left_sensor)

    def update(self):
        dx = self.direction * self.speed

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type, scale, *position):
        super().__init__()
        self.type = type
        self.scale = scale
        self.position = position


player1 = Jet('player', 500, 0, 10, 200, 8, 1, 0.35)
run = True

sleep(2)


while run:
    clock.tick(FPS)



    for i in range(0, tiles):
        screen.blit(bg, (0, i * bg_height - scroll))
    scroll -= 15

    player1.draw()
    player1.move(moving_left, moving_right)

    if (scroll) < 0:
        scroll = bg_height


    ### the ultrasonic values
    sensorTime = pygame.time.get_ticks()
    pevSensorTime = 0


    right, left = sensor_value()






    if right:
        moving_right = True
        moving_left = False


    if left:
        moving_left = True
        moving_right = False

    if not left and  not right:
        moving_left = False
        moving_right = False
 











    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            run = False




        #if the keys are pressesd

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True

            if event.key == pygame.K_a:
                moving_left = True

            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False

            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
