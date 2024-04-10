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
        self.img = pygame.transform.scale(pygame.image.load('pik.png'), (50, 60))
        self.speed = 1
        self.life = 100
        self.atk = 10
        
        self.surf = pygame.Surface((50, 60))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect()

        self.direction = 1
        self.pos = BaseWindow().vec(250,BaseWindow().hei//2)
        self.vel = BaseWindow().vec(0,0)
        self.acc = BaseWindow().vec(0,0)

        self.fric = BaseWindow().FRIC

    def move(self , camera_offset_x):
        lastacc = self.acc
        lastvel = self.vel
        lastpos = self.pos.x
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

        
        self.rect.midbottom = self.pos
        self.rect.midbottom += BaseWindow().vec(camera_offset_x,0)
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if hits[0].rect.top - P1.rect.bottom > -20:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top +1
            else:
                self.acc = lastacc
                self.vel = lastvel
                self.pos.x = lastpos
                self.rect.midbottom = self.pos
                self.rect.midbottom += BaseWindow().vec(camera_offset_x,0)
        if len(hits)>1:
            if hits[1].rect.top - P1.rect.bottom < -20:
                self.acc = lastacc
                self.vel = lastvel
                self.pos.x = lastpos
                self.rect.midbottom = self.pos
                self.rect.midbottom += BaseWindow().vec(camera_offset_x,0)
                if len(hits)>2:
                    self.vel.y = 0
                    self.pos.y = hits[0].rect.top +1
        

        
        self.fric = BaseWindow().FRIC

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -15
    
    def dash(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if hits:
            self.img = pygame.transform.rotate(self.img, -90)
            self.vel.x += 30 * (1 if self.vel.x >= -0.01 else -1)
            return True
        return False
    
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
    def __init__(self, gameDisplay,niv:str):
        super().__init__()
        self.coords = open(f"level0_data.csv", "r", encoding='utf-8')
        self.length = 0
        self.tab = []
        self.tab_area = []
        self.gameDisplay = gameDisplay
        self.flip =  False
        self.rects = []
        self.images = []
        
        for x in open(f"level0_data.csv"):
            self.length += 1
            y = x.split(",")

            self.tab.append(y)

        for i in range(self.length):
            for j in range(80):
                if self.tab[i][j] == "0" or self.tab[i][j] == "1" or self.tab[i][j] == "2" or self.tab[i][j] == "3" or self.tab[i][j] == "4" or self.tab[i][j] == "5":
                    self.image = pygame.transform.scale(pygame.image.load(rf'img/tile/{self.tab[i][j]}.png'), (68, 68))
                    self.gameDisplay.blit(self.image, (500,500))
                    self.images.append(self.image)
                    rect = Platform(68,68, j*68, i*68)
                    platforms.add(rect)
                    self.rects.append(rect)


    def draw(self, camera_offset_x):
        for i in range( 0, len(self.rects)):
            self.rects[i].move(camera_offset_x)
            self.gameDisplay.blit(pygame.transform.flip(self.images[i], self.flip, False), self.rects[i].rect.topleft)
                
class Platform(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self,  w,h,x, y):
        super().__init__()
        self.surf = pygame.Surface((w,h))
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
    def move(self,camera_offset_x):
        self.rect = self.surf.get_rect(topleft = (self.x + camera_offset_x, self.y))

def setup_imgs(window_width, window_height):
    # background image
    background = pygame.transform.scale(pygame.image.load(r'bg2.jpg'), (window_width, window_height))

    # snowball image
    snowballimg = pygame.transform.scale(pygame.image.load(r'snowball.png'), (20, 20))

    return background, snowballimg

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
    update_time = pygame.time.get_ticks()
    frame_index = 0
    s = [] 

    n = Niveau(gameDisplay, "niv2")

    while running:
        
        # update anim

        camera_offset_x = BaseWindow().wid // 8 - P1.pos.x - 25

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

        P1.move(camera_offset_x)
        
        
        gameDisplay.blit(P1.surf, P1.rect)
        gameDisplay.blit(playerIMG, P1.rect)
        n.draw(camera_offset_x)

        for entity in s:

            gameDisplay.blit(snowballimg, entity.rect)
            entity.move()

        pygame.display.update() 
        clock.tick(BaseWindow().fps)

    #####################

P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)


platforms = pygame.sprite.Group()
playerIMG = Player().img
gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)
bg, snowballimg = setup_imgs(BaseWindow().wid, BaseWindow().hei)

gameDisplay.blit(bg, (0, 0))

play(gameDisplay, playerIMG)

pygame.quit()