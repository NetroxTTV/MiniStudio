import pygame, sys
import game

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
#pygame.mixer.init()  
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500), 0, 32)

font = pygame.font.SysFont(None, 20)

button_1_image = pygame.image.load('IMAGES/menu/Fichier 12.png')
button_1_image = pygame.transform.scale(button_1_image, (200, 50))
button_2_image = pygame.image.load('IMAGES/menu/Fichier 12.png')
button_2_image = pygame.transform.scale(button_2_image, (200, 50))
button_3_image = pygame.image.load('IMAGES/menu/Fichier 12.png')
button_3_image = pygame.transform.scale(button_3_image, (200, 50))
button_4_image = pygame.image.load('IMAGES/menu/Fichier 14.png')
button_4_image = pygame.transform.scale(button_4_image, (200, 50))
outline_image = pygame.image.load('IMAGES/menu/Fichier 2.png')  
outline_image = pygame.transform.scale(outline_image, (50, 60))  
outline_image_flipped = pygame.transform.flip(outline_image, True, False)

font_path = 'IMAGES/font/Norse.otf'  
font_size = 30 
custom_font = pygame.font.Font(font_path, font_size)

background_image = pygame.image.load('IMAGES/img/Plan_de_travail_1.png')
background_image = pygame.transform.scale(background_image, (500, 500))

def draw_text(text, font, color, surface, x, y, centered=False):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if centered:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

screen_width, screen_height = screen.get_size()
draw_text('Bonjour', custom_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2, centered=True)


sound_enabled = True  

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled

    print("Sound Enabled:", sound_enabled)

def change_resolution():
    global screen
    current_resolution = screen.get_size()
    if current_resolution == (500, 500):
        screen = pygame.display.set_mode((800, 600), 0, 32)
    else:
        screen = pygame.display.set_mode((500, 500), 0, 32)

def main_menu():
    largeur_ecran, hauteur_ecran = screen.get_size()
    # Pour le bouton "Jouer"
    button_1_x = (largeur_ecran - 200) // 2  
    button_1_y = 100  
    button_2_x = (largeur_ecran - 200) // 2
    button_2_y = 200   
    click = False
    while True:
        screen.blit(background_image, (0, 0))

        draw_text('God Ass Kicker', custom_font, (255, 255, 255), screen, largeur_ecran / 2, button_1_y + -70, centered=True)  

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(button_1_x, button_1_y, 200, 50)
        button_2 = pygame.Rect(button_2_x, button_2_y, 200, 50)


        if button_1.collidepoint((mx, my)):
            screen.blit(outline_image, (button_1_x + 50 - outline_image.get_width() + button_1_image.get_width(), button_1_y - 5))  # -5 pour centrer l'entourage autour du bouton
            screen.blit(outline_image_flipped, (button_1_x - 200 - outline_image_flipped.get_width() + button_1_image.get_width(), button_1_y - 5))
        screen.blit(button_1_image, (button_1_x, button_1_y))
        if button_2.collidepoint((mx, my)):
            screen.blit(outline_image, (button_2_x +200 , button_2_y ))  # -5 pour centrer l'entourage autour du bouton
            screen.blit(outline_image_flipped, (button_2_x - 200 - outline_image_flipped.get_width() + button_2_image.get_width(), button_2_y - 5))
        screen.blit(button_2_image, (button_2_x, button_2_y))

        draw_text('Jouer', custom_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 - 125, centered=True)
        draw_text('Options', custom_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 -24, centered=True)

        if button_1.collidepoint((mx, my)):
            if click:
                level_select()
        if button_2.collidepoint((mx, my)):
            if click:
                options()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def level_select():
    running = True

    map_image = pygame.image.load('IMAGES/menu/Map_God_Ass_Kicker_Danemark.png')
    map_image = pygame.transform.scale(map_image, (screen_width, screen_height))
    
    level_coords = [
        (195, 60),      #niveau 1
        (210, 120),     #niveau 2
        (250, 185),     #niveau 3
        (65, 210),     #niveau 4
        (140, 290),     #niveau 5
        (100, 400),     #niveau 6
        (195, 340),     #niveau 7
        (310, 440),     #niveau 8
        (320, 340),     #niveau 9
        (400, 270),     #niveau 10

    ]

    level_rects = [pygame.Rect(x, y, 50, 50) for x, y in level_coords]
    
    while running:
        screen.fill((0, 0, 0))
        screen.blit(map_image, (0, 0))  
        
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for i, level_rect in enumerate(level_rects):
                    if level_rect.collidepoint((mx, my)):
                        print(f"Lancement du niveau {i+1}")

                        pygame.quit()
                        game.Start_file(f"niv{i+1}")
                        


        #for level_rect in level_rects:
            #pygame.draw.rect(screen, (255, 0, 0), level_rect)  # Dessine un rectangle rouge.

        pygame.display.update()
        mainClock.tick(60)



        pygame.display.update()
        mainClock.tick(60)

def options():
    largeur_ecran, hauteur_ecran = screen.get_size()
    # Pour le bouton "Jouer"
    button_3_x = (largeur_ecran - 200) // 2  
    button_3_y = 100  
    button_4_x = (largeur_ecran - 200) // 2
    button_4_y = 200   
    click = False
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        draw_text('Options', custom_font, (255, 255, 255), screen, largeur_ecran / 2, button_3_y + -80, centered=True)

        mx, my = pygame.mouse.get_pos()

        button_3 = pygame.Rect(button_3_x, button_3_y, 200, 50)
        button_4 = pygame.Rect(button_4_x, button_4_y, 200, 50)

        if button_3.collidepoint((mx, my)):
            screen.blit(outline_image, (button_3_x + 50 - outline_image.get_width() + button_1_image.get_width(), button_3_y - 5))  # -5 pour centrer l'entourage autour du bouton
            screen.blit(outline_image_flipped, (button_3_x - 200 - outline_image_flipped.get_width() + button_1_image.get_width(), button_3_y - 5))
        screen.blit(button_1_image, (button_3_x, button_3_y))
        if button_4.collidepoint((mx, my)):
            screen.blit(outline_image, (button_4_x +200 , button_4_y ))  # -5 pour centrer l'entourage autour du bouton
            screen.blit(outline_image_flipped, (button_4_x - 200 - outline_image_flipped.get_width() + button_2_image.get_width(), button_4_y - 5))
        screen.blit(button_2_image, (button_4_x, button_4_y))


        draw_text('Son', custom_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 - 125, centered=True)
        draw_text('Resolution', custom_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 -24, centered=True)

        if button_3.collidepoint((mx, my)):
            if click:
                toggle_sound()
        if button_4.collidepoint((mx, my)):
            if click:
                change_resolution()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

main_menu()