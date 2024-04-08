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
        self.wid = 1020
        self.hei = 580
        self.fps = 160
        self.ACC = 1
        self.FRIC = -0.14
        self.FramePerSec = pygame.time.Clock()
        self.vec = pygame.math.Vector2 

class Player(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self):
        super().__init__()
        self.img = pygame.transform.scale(pygame.image.load('img/pik.png'), (80, 80))
        self.speed = 1
        self.life = 100
        self.atk = 10
        
        self.surf = pygame.Surface((50, 80))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect()

        self.direction = 1
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
                self.direction = -1
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
                
                self.pos.y = hits[0].rect.top +1
                if len(hits) > 1:
                    if hits[1].rect.right - P1.pos[0] > 0 :
                        self.vel.x = 0
                    
                        self.pos.x = hits[1].rect.right +1
            

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15
    
    def dash(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if hits:
            self.img = pygame.transform.rotate(self.img, -90)
            self.vel.x += 30 * (1 if self.vel.x >= -0.01 else -1)
            return True
        return False
    
    def slide(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if hits:
            self.fric = -0.009

class Axe(pygame.sprite.Sprite):
    def __init__(self, Playerpos):
        super().__init__()
        
        self.surf = pygame.Surface((60,30))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.img = pygame.transform.scale(pygame.image.load('img/pik.png'), (60, 30))

        self.pos = Playerpos

class Snowball(pygame.sprite.Sprite):
    def __init__(self, x, y, targetx, targety):
        super().__init__()

        self.speed = 10
        
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()
        self.img = pygame.transform.scale(pygame.image.load('img/snowball.png'), (20, 20))

        self.rect.midbottom = P1.rect.midbottom

        self.angle = math.atan2(targety-y, targetx-x) 

        self.dir = BaseWindow().vec(math.cos(self.angle)*self.speed,math.sin(self.angle)*self.speed)
        self.acc = BaseWindow().vec(0,0)
        self.vel = self.dir
        self.pos = BaseWindow().vec((x, y))

    def move(self):
        self.acc = BaseWindow().vec(0,0.1)

        self.acc.x += self.vel.x * -0.001
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        self.rect.center = self.pos

class Platform(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self,  w,h,x, y):
        super().__init__()
        self.surf = pygame.Surface((w,h))
        self.surf.fill((100,100,100))
        self.rect = self.surf.get_rect(center = (x,y))
 
def setup_imgs(window_width, window_height):
    # background image
    background = pygame.transform.scale(pygame.image.load('img/bg2.jpg'), (window_width, window_height))

    return background

def gd(window_width, window_height): # PAS TOUCHE
    gd = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('PIKMIN')
    return gd
    
def play(gameDisplay):
    
    clock = pygame.time.Clock()
    startCD = pygame.time.get_ticks()
    lastsnowball = startCD
    cooldownsnowball = 500  #ms

    lastdash = startCD
    cooldowndash = 1000 #ms

    lastaxe = startCD
    cooldownaxe = 1000#ms
    ChargeStart = 0


    AxeBaseActive = False
    sliding = False
    running = True
    snowballs = []

    while running:
        
        
        for event in pygame.event.get():

##################### CLICK CHECK ##################### 
            
            if pygame.mouse.get_pressed()[0]:
                now = pygame.time.get_ticks()
                if now - lastsnowball >= cooldownsnowball:
                    lastsnowball = now
                    x,y = pygame.mouse.get_pos()
                    snowball = Snowball(P1.rect.midbottom[0] - 25, P1.rect.midbottom[1] -25,  x,y )
                    AtksP.add(snowball)
                    snowballs.append(snowball)

            
            if pygame.mouse.get_pressed()[2]:
                ChargeStart += 10
                print(ChargeStart)
            if not(pygame.mouse.get_pressed()[2]):
                if ChargeStart >= 600 and not(AxeBaseActive):
                    now = pygame.time.get_ticks()
                    lastaxe = now
                    AxeBaseActive = True

                elif ChargeStart >= 60 and not(AxeBaseActive):
                    now = pygame.time.get_ticks()
                    lastaxe = now
                    AxeBaseActive = True

                ChargeStart = 0
                
            
#######################################################
################### PLAYER MOVEMENT ###################
                    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                pygame.QUIT
                running = False
            if keys[pygame.K_SPACE]:
                P1.jump()
            
            if keys[pygame.K_LSHIFT]:
                now = pygame.time.get_ticks()
                if now - lastdash >= cooldowndash and -10 < P1.vel.x < 10 and not(sliding):
                    lastdash = now
                    sliding = P1.dash()
            

#######################################################
################# GAME UPDATE/DISPLAY #################

        now = pygame.time.get_ticks()

        if now - lastdash >= (cooldowndash //5)  and sliding:
            P1.img = pygame.transform.rotate(P1.img, 90)
            sliding = False
        if now - lastaxe >= (cooldownaxe/2) and AxeBaseActive:
            AxeBaseActive = False
        else:
            AXE.rect.center = P1.rect.center + BaseWindow().vec((50*P1.direction,15))

        
        P1.move()
        P1.update()
        

        gameDisplay.fill((0,0,0))
        gameDisplay.blit(bg, (0, 0))

        gameDisplay.blit(P1.surf, P1.rect)
        gameDisplay.blit(P1.img, P1.rect)
        gameDisplay.blit(PT1.surf, PT1.rect)
        gameDisplay.blit(PT2.surf, PT2.rect)

        if AxeBaseActive:
            gameDisplay.blit(AXE.surf, AXE.rect)

        for entity in snowballs:
            entity.move()
            gameDisplay.blit(entity.img, entity.rect)
            
        pygame.display.update() 
        clock.tick(BaseWindow().fps)
        
#######################################################

PT1 = Platform(BaseWindow().wid, 20,BaseWindow().wid/2, BaseWindow().hei - 100)
PT2 = Platform(60, 500,500,500)
P1 = Player()
AXE = Axe(P1.pos)


all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(PT2)
all_sprites.add(P1)
all_sprites.add(AXE)


platforms = pygame.sprite.Group()
platforms.add(PT1)
platforms.add(PT2)

AtksP = pygame.sprite.Group()
AtksP.add(AXE)


AtksE = pygame.sprite.Group()


bg = setup_imgs(BaseWindow().wid, BaseWindow().hei)
gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)


play(gameDisplay)

pygame.quit()
