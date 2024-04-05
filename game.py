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

        self.fric = BaseWindow().FRIC

    def move(self):
        self.acc = BaseWindow().vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_s]:
            self.slide()
        else:
            if pressed_keys[K_q]:
                self.acc.x = -BaseWindow().ACC
                self.direction = 0
            if pressed_keys[K_d]:
                self.acc.x = BaseWindow().ACC
                self.direction = 1
             
        self.acc.x += self.vel.x * self.fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > BaseWindow().wid:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = BaseWindow().wid
            
        self.rect.midbottom = self.pos
        self.fric = BaseWindow().FRIC

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
    
    def dash(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if hits:
            self.vel.x += 30 * (1 if self.vel.x >= -0.01 else -1)
    
    def slide(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if hits:
            self.fric = -0.009

class snowball:
    def __init__(self, x, y, targetx, targety):
        self.speed = 20
    
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()

        self.rect.midbottom = P1.rect.midbottom
        self.point = pygame.mouse.get_pos()

        self.angle = math.atan2(targety-y, targetx-x) 

        self.dir = BaseWindow().vec(math.cos(self.angle)*self.speed,math.sin(self.angle)*self.speed)
        self.acc = BaseWindow().vec(0,0)
        self.vel = self.dir
        self.pos = BaseWindow().vec((x, y))

    def move(self):
        self.acc = BaseWindow().vec(0,0.3)
        

        self.acc.x += self.vel.x * -0.001
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        self.rect.center = self.pos

class Niveau(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coords = open("level0_data.csv", "r", encoding='utf-8')
        self.length = 0
        self.tab = []
        self.tab_area = []
        
        for x in open("level0_data.csv"):
            self.length += 1
            y = x.split(",")

            self.tab.append(y)

    def Level(self):
        for i in range(self.length):
            for j in range(30):
                if self.tab[i][j] == "0":
                    self.tab_area.append([i, j])
                    self.tab_area
        return self.tab_area

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
    lastsnowball = pygame.time.get_ticks()
    cooldownsnowball = 0  #ms
    lastdash = pygame.time.get_ticks()
    cooldowndash = 1000 #ms
    sliding = False
    running = True
    s = []

    while running:

        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(bg, (0, 0))
        
        for event in pygame.event.get():

################### CLICK CHECK ################### 
            
            if pygame.mouse.get_pressed()[0]:
                now = pygame.time.get_ticks()
                if now - lastsnowball >= cooldownsnowball:
                    lastsnowball = now
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
            
            if keys[pygame.K_LSHIFT]:
                now = pygame.time.get_ticks()
                if now - lastdash >= cooldowndash and -10 < P1.vel.x < 10:
                    lastdash = now
                    playerIMG = pygame.transform.rotate(playerIMG, -90)
                    sliding = True
                    P1.dash()
            now = pygame.time.get_ticks()
            if now - lastdash >= (cooldowndash //30)  and sliding:
                playerIMG = pygame.transform.rotate(playerIMG, 90)
                sliding = False

                

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

p = Niveau().Level()
print(p)

bg, playerIMG, snowballimg = setup_imgs(BaseWindow().wid, BaseWindow().hei)
gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)
play(gameDisplay, playerIMG)

pygame.quit()