import pygame
import random

class ennemy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed):
        #main variables
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.alive = True
        self.speed = speed
        self.jump = False
        self.direction = 1
        self.vel_y = False
        self.flip = False
        self.animation_list =[]
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #walking animation
        for i in range(1,10):
            img = pygame.image.load(f'IMAGES/ennemy walking/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()*0.07), int(img.get_height()*0.07)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        #rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
    def move(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0

        #assign movement variable if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump == True:
            self.vel_y = -11
            self.jump = False

        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #check collision with the floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    

    def update_animation(self):
        ANIMATION_COOLDOWN = 125
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, camera_offset_x):
        self.rect.move(camera_offset_x,0)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect )
        


def start_e(char, x, y, speed):
    global E1
    global GRAVITY
    global screen
    screen = pygame.display.set_mode((1920,1080))

    pygame.init()
    clock = pygame.time.Clock()
    FPS = 60
    GRAVITY = 0.75

    E1 = ennemy(char, x, y, speed)
    run = True


        
