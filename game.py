import pygame
import time
#from sol import Sol
pygame.init()

class BaseWindow:
    def __init__(self) -> None:
        self.wid = 1920
        self.hei = 1080
        self.fps = 120

class Player:
    def __init__(self) -> None:
        self.x = (BaseWindow().wid)//2
        self.y = (BaseWindow().hei)//2
        self.speed = 1
        self.life = 100
        self.atk = 10
        
    def gravity(self):
        self.y += 3.2 

    def player(self, x, y):
        gameDisplay.blit(playerIMG, (x, y))

def setup_imgs(window_width, window_height):
    # background image
    background = pygame.transform.scale(pygame.image.load(r'bg2.jpg'), (window_width, window_height))

    # player image + rotate
    img = pygame.transform.scale(pygame.image.load(r'pik.png'), (100, 100))
    playerI = pygame.transform.rotate(img, 0)

    return background, playerI

def gd(window_width, window_height):
    gd = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('Space Crashers')
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
            if keys[pygame.K_z]:
                    playerY -= 500 * dt
            if keys[pygame.K_s]:
                    playerY += 500 * dt
            if keys[pygame.K_q]:
                    playerX -= 500 * dt
            if keys[pygame.K_d]:
                    playerX += 500 * dt
        pygame.display.update() 
        clock.tick(BaseWindow().fps)
    #####################

bg, playerIMG = setup_imgs(BaseWindow().wid, BaseWindow().hei)
gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)
play(gameDisplay, Player().x, Player().y)

pygame.quit()