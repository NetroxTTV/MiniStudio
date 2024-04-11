import pygame
import random

pygame.init()
screenWidth = 800
screenHeight = int(screenWidth * 0.8)

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
scroll_thresh = 200
ROWS = 16
COLS = 150
TILE_SIZE = screenHeight // ROWS
TILE_SIZE = 21
screen_scroll = 0
bg_scroll = 0

#define player action variable
moving_left = False
moving_right = False
shoot = False
alive = True

#load image
bg_img = pygame.image.load('cloud.jpg').convert_alpha()

lance_img = pygame.image.load('throwing_lance/lance.png').convert_alpha()
lance_img = pygame.transform.scale(lance_img, (int(lance_img.get_width()*0.07), int(lance_img.get_height()*0.07)))

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 255)

def draw_bg():
    screen.fill(BG)
    screen.blit(bg_img, (0,0))
    pygame.draw.line(screen, RED, (0, 300), (screenWidth*2, 300), 5)

# class Camera:
#     position = (0, 0)

#     default_speed = 10
#     direction = 0

#     @staticmethod
#     def update(dt):
#         Camera.position += Camera.default_speed * Camera.direction * dt

#     def move(direction):
#         Camera.direction = direction


class character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        #main variables
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.direction = 1
        self.vel_y = False
        self.jump = False
        self.in_air = False
        self.flip = False
        self.animation_list =[]
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        #standing animation
        for i in range(1,13):
            img = pygame.image.load(f'character animation/standing animation/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        #rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #health
        self.health = 6
        self.max_health = 6


    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health <= 0:
            alive = False

    def get_health(self, amount):
        if self.health < self.max_health:
            self.health += amount
        if self.health >= self.max_health:
            self.health = self.max_health

    # def full_hearts(self):
    #     for heart in range(self.health):
    #         screen.blit(full_heart, (heart * 30 + 10, 25))

    # def empty_hearts(self):
    #     for heart in range(self.max_health):
    #         if heart < self.health:
    #             screen.blit(full_heart, (heart * 50 +10,5))
    #         else:
    #             screen.blit(empty_heart, (heart * 50 +10,5))

    def half_heart(self):
        half_heart_total = self.health / 2
        half_heart_exists = half_heart_total - int(half_heart_total) != 0

        for heart in range(int(self.max_health / 2)):
            if int(half_heart_total) > heart:
                screen.blit(full_heart, (heart * 30 + 10, 25))
            elif half_heart_exists and int(half_heart_total) == heart:
                screen.blit(half_heart, (heart * 30 + 10, 25))
            else:
                screen.blit(empty_heart, (heart * 30 + 10, 25))

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
            self.vel_y = -15
            self.in_air = True
            self.jump = False

        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #check collision with the floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 100
            lance = Lance(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction * self.flip), self.rect.centery, self.direction)
            lance_group.add(lance)
            pygame.draw.rect(screen, RED, lance_rect)
            lance = screen.blit(pygame.transform.flip(lance_weapon, self.flip, False), self.rect)

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    
    def update(self):
        self.update_animation()
        self.half_heart()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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
            img = pygame.image.load(f'ennemy walking/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width()*0.07), int(img.get_height()*0.07)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        #rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #health
        self.health = 10
        self.max_health = 10
        #create ai specific
        self.vision = pygame.Rect(0,0,400,20)
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health <= 0:
            self.alive = False
 
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

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 100
            lance = Lance(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            lance_group.add(lance)
            lance = screen.blit(pygame.transform.flip(lance_img, self.flip, False), self.rect)

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

    def ai(self):
        if self.alive and character.alive:
            if self.idling == False and random.randint(0, 1000) == 1:
                self.update_action(0) #0 = Idle
                self.idling = True
                self.idling_counter = 50
            # check if the ai is near the player
            if self.vision.colliderect(character.rect()):
                    self.update_action(0) #Idle
                    #shoot
                    self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) #1 = Walk
                    self.move_counter += 1
                    #update ennemy vision
                    self.vision.center = (self.rect.centerx + 200 * self.direction, self.rect.centery)
                    pygame.draw.rect(screen, RED, self.vision)

                    if self.move_counter > TILE_SIZE*2:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -=1
                    if self.idling_counter == 0:
                        self.idling = False

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Lance(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = lance_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #move lance
        self.rect.x += (self.direction * self.speed)
        #check if bullet is going off screen
        if self.rect.right < 0 or self.rect.left > screenWidth-100:
            self.kill()
        #check if collision with player
        if pygame.sprite.spritecollide(character, lance_group, False):
            if character.alive:
                character.health -= 1
                self.kill()


#create sprite groups
lance_group = pygame.sprite.Group()

yellowPikmin = character('player', screenWidth/2, screenHeight/2, 0.7, 5)
link = pygame.sprite.GroupSingle(yellowPikmin)
chess_piece = ennemy('ennemy', 300, 300, 3)

#heart
full_heart = pygame.image.load('character animation/heart/fullheart.png').convert_alpha()
full_heart = pygame.transform.scale(full_heart, (int(full_heart.get_width()*2), int(full_heart.get_height()*2)))

half_heart = pygame.image.load('character animation/heart/halfheart.png').convert_alpha()
half_heart = pygame.transform.scale(half_heart, (int(half_heart.get_width()*2), int(half_heart.get_height()*2)))

empty_heart = pygame.image.load('character animation/heart/emptyheart.png').convert_alpha()
empty_heart = pygame.transform.scale(empty_heart, (int(empty_heart.get_width()*2), int(empty_heart.get_height()*2)))


run = True

class World:
    world_elements = []

    def Update(self):
        pass

    def Draw(self):
        #afficher tous les éléments
        pass

while run:

    clock.tick(FPS)

    draw_bg()
    
    # camera_direction_x = yellowPikmin.get_in_scroll_zone()
    # Camera.move(camera_direction_x * (1, 0))
    # Camera.update(0.016)

    yellowPikmin.update()
    yellowPikmin.draw()

    chess_piece.ai()
    chess_piece.update_animation()
    chess_piece.draw()
    screen_scroll = yellowPikmin.move(moving_left, moving_right)

    #update and draw groups
    lance_group.update()
    lance_group.draw(screen)

    # update player action
    if yellowPikmin.alive:
        if shoot:
            yellowPikmin.shoot()

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                moving_left = True
            if event.key == pygame.K_t:
                yellowPikmin.get_damage(1)
            if event.key == pygame.K_y:
                yellowPikmin.get_health(1)
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_z and yellowPikmin.alive and yellowPikmin.in_air == False:
                yellowPikmin.jump = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_ESCAPE:
                run = False
        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    link.update()
    pygame.display.update()

pygame.quit()