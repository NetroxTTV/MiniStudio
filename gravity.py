import pygame
from pygame.locals import *
import sys

pygame.init()
 
vec = pygame.math.Vector2 
HEIGHT = 550
WIDTH = 1000
ACC = 1
FRIC = -0.14
FPS = 60
FramePerSec = pygame.time.Clock()

img = pygame.transform.scale(pygame.image.load(r'pik.png'), (80, 80))
bg = pygame.transform.scale(pygame.image.load(r'bg2.jpg'), (WIDTH, HEIGHT))


displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((80, 80))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.direction = 0 #0 = right 1 = left
        self.fric = FRIC
 
    def move(self):
        self.acc = vec(0,1)

        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_s]:
            self.slide()
        else:
            if pressed_keys[K_q]:
                self.acc.x = -ACC
                self.direction = 0
            if pressed_keys[K_d]:
                self.acc.x = ACC
                self.direction = 1

             
        self.acc.x += self.vel.x * self.fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.midbottom = self.pos

        self.fric = FRIC
        

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
        if hits and -10 < self.vel.x < 10:
            self.vel.x *= 5
    
    def slide(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if hits:
            self.fric = -0.0004


    
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((100,100,100))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 

PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
            if event.key == pygame.K_LSHIFT:
                P1.dash()
     
    displaysurface.fill((0,0,0))
    P1.move()

    P1.update()

    displaysurface.blit(bg, (0, 0))
    displaysurface.blit(img, P1.rect)
    displaysurface.blit(PT1.surf, PT1.rect)
    
    pygame.display.update()
    FramePerSec.tick(FPS)