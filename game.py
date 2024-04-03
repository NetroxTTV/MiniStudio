import pygame
import time
from pygame.locals import *
import sys
import math
import random
#from sol import Sol
pygame.init()

class BaseWindow(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self) -> None:
        super().__init__()
        self.wid = 1920
        self.hei = 1080
        self.fps = 120
        self.ACC = 1
        self.FRIC = -0.14
        self.FramePerSec = pygame.time.Clock()
        self.vec = pygame.math.Vector2 

class Player(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self):
        super().__init__() 
        self.speed = 1
        self.life = 100
        self.atk = 10
        
        self.surf = pygame.Surface((80, 80))
        self.rect = self.surf.get_rect()
   
        self.pos = BaseWindow().vec((1920/2, 1080/2))
        self.vel = BaseWindow().vec(0,0)
        self.acc = BaseWindow().vec(0,0)

    def move(self):
        self.acc = BaseWindow().vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_q]:
            self.acc.x = -BaseWindow().ACC
            
        if pressed_keys[K_d]:
            self.acc.x = BaseWindow().ACC
             
        self.acc.x += self.vel.x * BaseWindow().FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > BaseWindow().wid:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = BaseWindow().wid
            
        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if P1.vel.y > 0:        
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
    	
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15
    
    def slide(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if hits and -10 < self.vel.x < 10:
            self.vel.x *= 5
        elif not(hits):
            self.vel.y += 30

class snowball:
    def __init__(self, x, y, targetx, targety):
        self.speed = 6
    
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()

        self.rect.midbottom = P1.rect.midbottom
        self.point = pygame.mouse.get_pos()

        self.angle = math.atan2(targety-y, targetx-x) 

        self.dx = math.cos(self.angle)*self.speed
        self.dy = math.sin(self.angle)*self.speed
        self.x = x
        self.y = y

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy 
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

class platform(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((BaseWindow().wid, 20))
        self.surf.fill((100,100,100))
        self.rect = self.surf.get_rect(center = (BaseWindow().wid/2, BaseWindow().hei - 10))
 
def setup_imgs(window_width, window_height):
    # background image
    background = pygame.transform.scale(pygame.image.load(r'bg2.jpg'), (window_width, window_height))

    # player image + rotate
    img = pygame.transform.scale(pygame.image.load(r'pik.png'), (80, 80))
    playerI = pygame.transform.rotate(img, 0)

    # snowball image
    snowballimg = pygame.transform.scale(pygame.image.load(r'snowball.png'), (20, 20))

    return background, playerI, snowballimg

def gd(window_width, window_height): # PAS TOUCHE
    gd = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('PIKMIN')
    return gd
    
def play(gameDisplay, playerIMG):
    
    clock = pygame.time.Clock()
    running = True
    s = []

    while running:

        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(bg, (0, 0))
        
        for event in pygame.event.get():

################### CLICK CHECK ################### 
            
            if pygame.mouse.get_pressed()[0]:
                x,y = pygame.mouse.get_pos()
                s.append(snowball(P1.rect.midbottom[0] - 25, P1.rect.midbottom[1] -25,  x,y ))
                snowball(P1.rect.midbottom[0] - 25, P1.rect.midbottom[1] - 25,  x,y)
################### PLAYER MOVEMENT ################### 
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                pygame.QUIT
                running = False
            if keys[pygame.K_SPACE]:
                P1.jump()
            if keys[pygame.K_s]:
                playerIMG = pygame.transform.rotate(playerIMG, -90)
                P1.slide()

        gameDisplay.fill((0,0,0))
        P1.move()
        P1.update()

        gameDisplay.blit(bg, (0, 0))
        gameDisplay.blit(playerIMG, P1.rect)
        gameDisplay.blit(PT1.surf, PT1.rect)
        for entity in s:

            gameDisplay.blit(snowballimg, entity.rect)
            entity.move()

        pygame.display.update() 
        clock.tick(BaseWindow().fps)

    #####################

PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

bg, playerIMG, snowballimg = setup_imgs(BaseWindow().wid, BaseWindow().hei)
gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)
play(gameDisplay, playerIMG)

pygame.quit()
