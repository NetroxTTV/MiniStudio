import pygame
import time
from pygame.locals import *
import sys
import math
import random
import ennemi

pygame.init()
clock = pygame.time.Clock()

class FPSCounter:
    def __init__(self, surface, font, clock, color, pos):
        self.surface = surface
        self.font = font
        self.clock = clock
        self.pos = pos
        self.color = color

        self.fps_text = self.font.render(str(int(self.clock.get_fps())) + "FPS", False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

    def render(self):
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        text = f"{self.clock.get_fps():2.0f} FPS"
        self.fps_text = self.font.render(text, False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

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

class spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]

class Player(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self, niveau):
        super().__init__()
        self.speed = 1
        self.life = 100
        self.atk = 10
        self.niveau = niveau
        
        self.surf = pygame.Surface((100, 130))
        self.surf.fill((0,0,0))
    
        self.rect = self.surf.get_rect()

        self.direction = 1
        self.pos = BaseWindow().vec(250,BaseWindow().hei//2)
        self.vel = BaseWindow().vec(0,0)
        self.acc = BaseWindow().vec(0,0)

        self.fric = BaseWindow().FRIC
        self.sliding = False
        
        self.flip = False

    def move(self , camera_offset_x):
        lastacc = self.acc
        lastvel = self.vel
        lastpos = self.pos.x
        self.acc = BaseWindow().vec(0,0.5)

        pressed_keys = pygame.key.get_pressed()  
        if pressed_keys[K_s]:
            self.slide()
        else:
            self.sliding = False
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
            self.fric = 0.01
            self.sliding = True

    def check_died(self):
        if self.pos.y >= 1150:
            self.pos = BaseWindow().vec(250,BaseWindow().hei//2)

    def check_end(self):
        if self.pos.x >= 5127:
            pygame.quit()
            sys.exit()
            
class Axe(pygame.sprite.Sprite):
    def __init__(self, Playerpos):
        super().__init__()
        
        self.surf = pygame.Surface((60,30))
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect()
        self.img = pygame.transform.scale(pygame.image.load('IMAGES/img/pik.png'), (60, 30))

        self.pos = Playerpos
        
class Snowball(pygame.sprite.Sprite):
    def __init__(self, x, y, targetx, targety):
        super().__init__()

        self.speed = 10
        
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()
        self.img = pygame.transform.scale(pygame.image.load('IMAGES/img/snowball.png'), (20, 20))

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
        self.coords = open(f"IMAGES/niveau/{niv}.csv", "r", encoding='utf-8')
        self.length = 0
        self.tab = []
        self.tab_area = []
        self.gameDisplay = gameDisplay
        self.flip =  False
        self.rects = []
        self.images = []
        
        for x in open(f"IMAGES/niveau/{niv}.csv"):
            self.length += 1
            y = x.split(",")

            self.tab.append(y)

        for i in range(self.length):
            for j in range(80):
                if self.tab[i][j] == "0" or self.tab[i][j] == "1" or self.tab[i][j] == "2" or self.tab[i][j] == "3" or self.tab[i][j] == "4" or self.tab[i][j] == "5" or self.tab[i][j] == "6" or self.tab[i][j] == "7" or self.tab[i][j] == "8" or self.tab[i][j] == "9" or self.tab[i][j] == "10":
                    self.image = pygame.transform.scale(pygame.image.load(rf'IMAGES/img/tile/{self.tab[i][j]}.png'), (68, 68))
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
    
def play(gameDisplay, niv, fps_counter):
    startCD =  pygame.time.get_ticks()

    lastsnowball = startCD
    cooldownsnowball = 300#ms
    snowballs = []
    
    lastaxe = startCD
    cooldownaxe = 2000#ms

    nowframe = 0
    
    AxeBaseActive = False
    n = Niveau(gameDisplay, niv)
    running = True  
    while running:
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
                    
        if AxeBaseActive:
            gameDisplay.blit(AXE.surf, AXE.rect)
            
        n.draw(camera_offset_x)

        if P1.sliding and (P1.vel.x > 0.1 or P1.vel.x < -0.1):
            nowframe += 0.1
            if nowframe >= len(sliding_stance):
                nowframe = 0
            frame = sliding_stance[int(nowframe)]

        elif P1.vel.x > 0.1 or P1.vel.x < -0.1:
            nowframe += 0.12
            if nowframe >= len(running_stance):
                nowframe = 0
            frame = running_stance[int(nowframe)]
            
        else:
            nowframe += 0.15
            if nowframe >= len(base_stance):
                nowframe = 0
            frame = base_stance[int(nowframe)]
                    
        image = pygame.transform.scale(frame, (int(frame.get_width()*0.5), int(frame.get_height()*0.5)))
        image = pygame.transform.flip(image, P1.flip, False)
        image_rect = (P1.rect[0] - image.get_width()/8 ,P1.rect[1],image.get_width(),image.get_height())
        gameDisplay.blit(image,image_rect)

        for entity in snowballs:

            gameDisplay.blit(entity.img , entity.rect)
            entity.move()
        
        ennemi.E1.update_animation()
        ennemi.E1.draw(camera_offset_x)

        fps_counter.render()
        fps_counter.update()

        link.update()
        pygame.display.update() 
        clock.tick(100000) #fps
    
############################################################################# 
##########################    START FUNCTION    ############################# 
############################################################################# 

def Start_file(niv):
    global gameDisplay
    global bg
    global P1 
    global AXE
    global link
    global platforms
    global sliding_stance
    global running_stance
    global base_stance
    global E1

    gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)
    P1 = Player(niv)
    AXE = Axe(P1.pos)
    link = pygame.sprite.GroupSingle(P1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    platforms = pygame.sprite.Group()
    bg = pygame.transform.scale(pygame.image.load(r'IMAGES/img/background.png').convert_alpha(), (BaseWindow().wid, BaseWindow().hei))
    E1 = ennemi.start_e('ennemy', 1000, 100, 3)

    fps_counter = FPSCounter(gameDisplay, pygame.font.Font(None, 36), clock, (0, 0, 255), (150, 10))

    ss= spritesheet('IMAGES/animation/ANIMATIONS_SPRITESHEET.png')
    
    base_stance = []
    running_stance = []
    base_stance = ss.images_at([(0,62,351,269),(352,62,351,269),(704,62,351,269),(1056,62,351,269),(1408,62,351,269),(0,332,351,269),(352,332,351,269),(704,332,351,269),(1056,332,351,269),(1408,332,351,269),(0,602,351,269),(352,602,351,269)],colorkey=(0,255,0))
    running_stance = ss.images_at([(0,1412,351,269),(352,1412,351,269),(704,1412,351,269),(1056,1412,351,269),(1408,1412,351,269),(0,1682,351,269),(352,1682,351,269),(704,1682,351,269),(1056,1682,351,269),(1408,1682,351,269)],colorkey=(0,255,0))
    sliding_stance = ss.images_at([(0,872,351,269),(352,872,351,269),(704,872,351,269),(1056,872,351,269),(1408,872,351,269),(0,1142,351,269),(352,1142,351,269),(704,1142,351,269)],colorkey=(0,255,0))

    gameDisplay.blit(bg, (0, 0))
    play(gameDisplay, niv, fps_counter)

############################################################################# 
############################################################################# 
############################################################################# 

pygame.quit()