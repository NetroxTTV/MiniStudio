import pygame
import time
from pygame.locals import *
import sys
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
        self.x = (BaseWindow().wid)//2
        self.y = (BaseWindow().hei)//2
        self.speed = 1
        self.life = 100
        self.atk = 10
        
        self.surf = pygame.Surface((80, 80))
        self.rect = self.surf.get_rect()
   
        self.pos = BaseWindow().vec((10, 385))
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
        
    def gravity(self):
        self.y += 3.2 

    def player(self, x, y):
        gameDisplay.blit(playerIMG, (x, y))

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

    return background, playerI

def gd(window_width, window_height): # PAS TOUCHE
    gd = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('PIKMIN')
    return gd

def play(gameDisplay, playerX, playerY):
    
    clock = pygame.time.Clock()
    running = True
    dt = 0.01
    a = 0

    while running:

        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(bg, (0, 0))
        Player().player(playerX, playerY)
        
        for event in pygame.event.get():

################### CLICK CHECK ################### 
            
            point = pygame.mouse.get_pos()


            if pygame.mouse.get_pressed()[0]:
                a=a+1  
                time.sleep(0.1)
                pygame.draw.circle(bg, "red", point, 20, width=0)
                print("yes", a)


################### PLAYER MOVEMENT ################### 
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                pygame.QUIT
                running = False
            if keys[pygame.K_SPACE]:
                P1.jump()
            if keys[pygame.K_s]:
                P1.slide()
            if keys[pygame.K_q]:
                    playerX -= 500 * dt
            if keys[pygame.K_d]:
                    playerX += 500 * dt

        gameDisplay.fill((0,0,0))
        P1.move()
        P1.update()

        gameDisplay.blit(bg, (0, 0))
        gameDisplay.blit(playerIMG, P1.rect)
        gameDisplay.blit(PT1.surf, PT1.rect)

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

bg, playerIMG = setup_imgs(BaseWindow().wid, BaseWindow().hei)
gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)
play(gameDisplay, Player().x, Player().y)

pygame.quit()
