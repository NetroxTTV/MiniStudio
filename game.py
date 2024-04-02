import pygame
#from sol import Sol
pygame.init()

# INIT

FPS = 120
black = (0, 0, 0)
white = (255, 255, 255)
window_width = 1920
window_height = 1080
playerX = 0
playerY = 0

# background & player img

def player(playerX, playerY):
    gameDisplay.blit(playerIMG, (playerX, playerY))

def setup_imgs(window_width, window_height):
    # background image
    background = pygame.transform.scale(pygame.image.load(r'ressources/bg.jpg'), (window_width, window_height))

    # player image + rotate
    img = pygame.transform.scale(pygame.image.load(r'ressources/Pikmin_jaune_P3.png'), (100, 100))
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

    while running:
        # reset display
        gameDisplay.fill(black)
    
        # blit background
        gameDisplay.blit(bg, (0, 0))

        ### blit the player ###
        player(playerX, playerY)
        
        for event in pygame.event.get():
            # move player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                pygame.QUIT
                running = False
            
            #if !colliderect():
            if keys[pygame.K_z]:
                    playerY -= 300 * dt
            if keys[pygame.K_s]:
                    playerY += 300 * dt
            if keys[pygame.K_q]:
                    playerX -= 300 * dt
            if keys[pygame.K_d]:
                    playerX += 300 * dt
        
        pygame.display.update() 
        clock.tick(FPS)
    #####################

bg, playerIMG = setup_imgs(window_width, window_height)
gameDisplay = gd(window_width, window_height)
play(gameDisplay, playerX, playerY)

pygame.quit()
import pygame
#from sol import Sol
pygame.init()

# INIT

FPS = 120
black = (0, 0, 0)
white = (255, 255, 255)
window_width = 1920
window_height = 1080
playerX = 0
playerY = 0

# background & player img

def player(playerX, playerY):
    gameDisplay.blit(playerIMG, (playerX, playerY))

def setup_imgs(window_width, window_height):
    # background image
    background = pygame.transform.scale(pygame.image.load(r'ressources/bg.jpg'), (window_width, window_height))

    # player image + rotate
    img = pygame.transform.scale(pygame.image.load(r'ressources/Pikmin_jaune_P3.png'), (100, 100))
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

    while running:
        # reset display
        gameDisplay.fill(black)
    
        # blit background
        gameDisplay.blit(bg, (0, 0))

        ### blit the player ###
        player(playerX, playerY)
        
        for event in pygame.event.get():
            # move player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                pygame.QUIT
                running = False
            
            #if !colliderect():
            if keys[pygame.K_z]:
                    playerY -= 300 * dt
            if keys[pygame.K_s]:
                    playerY += 300 * dt
            if keys[pygame.K_q]:
                    playerX -= 300 * dt
            if keys[pygame.K_d]:
                    playerX += 300 * dt
        
        pygame.display.update() 
        clock.tick(FPS)
    #####################

bg, playerIMG = setup_imgs(window_width, window_height)
gameDisplay = gd(window_width, window_height)
play(gameDisplay, playerX, playerY)

pygame.quit()
