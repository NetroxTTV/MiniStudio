import pygame
import time
from pygame.locals import *
import sys
import math
import random
import temp
#from sol import Sol
pygame.init()

class BaseWindow(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self) -> None:
        super().__init__()
        self.wid = 1920
        self.hei = 1080
        self.fps = 120
        self.ACC = 0.8
        self.FRIC = -0.14
        self.FramePerSec = pygame.time.Clock()
        self.vec = pygame.math.Vector2 

class Player(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self):
        super().__init__()     

        
        self.direction = 1
        self.pos = BaseWindow().vec(250,BaseWindow().hei//2)
        self.vel = BaseWindow().vec(0,0)
        self.acc = BaseWindow().vec(0,0)

        self.fric = BaseWindow().FRIC
        self.health = 6
        self.max_health = 6
        self.flip = False

        self.animation_list =[]
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        #standing animation
        for i in range(1,13):
            img = pygame.image.load(f'standing_animation/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()*0.4), int(img.get_height()*0.4)))
            self.animation_list.append(img)
        
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

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
                self.flip = True
               
            if pressed_keys[K_d]:
                self.acc.x = BaseWindow().ACC
                self.direction = 1
                self.flip = False
                
             
        self.acc.x += self.vel.x * self.fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        
        self.rect.midbottom = self.pos
        self.rect.midbottom += BaseWindow().vec(camera_offset_x,0)
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for collision in hits:
                if collision.rect.top - self.rect.bottom > -27:
                    if collision.rect.center[0] - self.rect.center[0] > -60 and collision.rect.center[0] - self.rect.center[0] < 60:
                        self.vel.y = 0
                        self.pos.y = collision.rect.top +1
                        self.rect.midbottom = self.pos
                        self.rect.midbottom += BaseWindow().vec(camera_offset_x,0)
                else:
                    self.acc = lastacc
                    self.vel = lastvel
                    self.pos.x = lastpos
                    self.rect.midbottom = self.pos
                    self.rect.midbottom += BaseWindow().vec(camera_offset_x,0)
        

        
        self.fric = BaseWindow().FRIC

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for collision in hits:
                if collision.rect.top - self.rect.bottom > -3 and self.vel.y > -10:
                    self.vel.y = -15
    
    
    def slide(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if hits:
            self.fric = 0.000000000000000001

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def check_died(self):
        if self.pos.y >= 1150:
            self.pos = BaseWindow().vec(250,BaseWindow().hei//2)

    def check_end(self):
        print(self.pos.x)
        if self.pos.x >= 5127:
            temp.exec()
                    

    def draw(self):
        gameDisplay.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Axe(pygame.sprite.Sprite):
    def __init__(self, Playerpos):
        super().__init__()
        
        self.surf = pygame.Surface((60,30))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.img = pygame.transform.scale(pygame.image.load('pik.png'), (60, 30))

        self.pos = Playerpos
        
class Snowball(pygame.sprite.Sprite):
    def __init__(self, x, y, targetx, targety):
        super().__init__()

        self.speed = 10
        
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()
        self.img = pygame.transform.scale(pygame.image.load('snowball.png'), (20, 20))

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

class Niveau(pygame.sprite.Sprite):
    def __init__(self, gameDisplay,niv:str):
        super().__init__()
        self.coords = open(f"{niv}.csv", "r", encoding='utf-8')
        self.length = 0
        self.tab = []
        self.tab_area = []
        self.gameDisplay = gameDisplay
        self.flip =  False
        self.rects = []
        self.images = []
        
        for x in open(f"{niv}.csv"):
            self.length += 1
            y = x.split(",")

            self.tab.append(y)

        for i in range(self.length):
            for j in range(80):
                if self.tab[i][j] == "0" or self.tab[i][j] == "1" or self.tab[i][j] == "2" or self.tab[i][j] == "3" or self.tab[i][j] == "4" or self.tab[i][j] == "5" or self.tab[i][j] == "6":
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

def gd(window_width, window_height): # PAS TOUCHE
    gd = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('Game')
    return gd
    
def play(gameDisplay, niv):
    
    
    clock = pygame.time.Clock()
    startCD =  pygame.time.get_ticks()
    
    lastsnowball = startCD
    cooldownsnowball = 300#ms
    snowballs = []
    
    lastaxe = startCD
    cooldownaxe = 2000#ms
    
    AxeBaseActive = False
    n = Niveau(gameDisplay, niv)
    running = True  
    while running:
        
        clock.tick(BaseWindow().fps)

        # update anim

        P1.update_animation()
        P1.draw()

        camera_offset_x = BaseWindow().wid // 6 - P1.pos.x - 25

        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(bg, (0, 0))
        
        for event in pygame.event.get():

##################### CLICK CHECK ##################### 
            
            now = pygame.time.get_ticks()
            
            if pygame.mouse.get_pressed()[0]:
                if now - lastsnowball >= cooldownsnowball:
                    lastsnowball = now
                    x,y = pygame.mouse.get_pos()
                    snowballs.append(Snowball(P1.rect.midbottom[0] - 25, P1.rect.midbottom[1] -25,  x,y ))
                    Snowball(P1.rect.midbottom[0] - 25, P1.rect.midbottom[1] - 25,  x,y)
            
            if pygame.mouse.get_pressed()[2]:
                if now - lastaxe >= cooldownaxe:
                    lastaxe = now
                    AxeBaseActive = True

#######################################################
################### PLAYER MOVEMENT ###################
            
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                pygame.QUIT
                running = False
            if keys[pygame.K_SPACE]:
                P1.jump()
                
#######################################################
################# GAME UPDATE/DISPLAY #################

        P1.move(camera_offset_x)
        P1.check_died()
        P1.check_end()
        
        if pygame.time.get_ticks() - lastaxe >= (cooldownaxe/2) and AxeBaseActive:
            AxeBaseActive = False
        else:
            AXE.rect.center = P1.rect.center + BaseWindow().vec((50*P1.direction,15))
            
        #gameDisplay.blit(playerIMG, P1.rect)
        #gameDisplay.blit(playerIMG, P1.rect)
        
        P1.draw()
        
        if AxeBaseActive:
            gameDisplay.blit(AXE.surf, AXE.rect)
            
        n.draw(camera_offset_x)

        for entity in snowballs:

            gameDisplay.blit(entity.img , entity.rect)
            entity.move()
        link.update()
        pygame.display.update() 
    
#######################################################

def Start_file(niv):
    print(niv, "aaaa")
    global gameDisplay
    global bg
    global P1 
    global AXE
    global link
    global platforms

    gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)
    P1 = Player()
    AXE = Axe(P1.pos)
    link = pygame.sprite.GroupSingle(P1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    platforms = pygame.sprite.Group()
    bg = pygame.transform.scale(pygame.image.load(r'img/background.png').convert_alpha(), (BaseWindow().wid, BaseWindow().hei))
    playerIMG = Player().image
    gameDisplay.blit(bg, (0, 0))
    play(gameDisplay, niv)




pygame.quit()