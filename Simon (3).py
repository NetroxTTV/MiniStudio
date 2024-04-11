import pygame

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
alive = False

#load image
bg_img = pygame.image.load('cloud.jpg').convert_alpha()

#snow
snow_img = pygame.image.load('snowball.png').convert_alpha()

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
        self.direction = 1
        self.vel_y = False
        self.jump = False
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
        
        # def basic_health(self):
        #     pygame.draw.rect(screen, (200,0,0), (10,10,self.hp/self.ratio, 25))
        #     pygame.draw.rect(screen, (255,255,255), (10,10,self.health_bar_length, 25), 4)


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


    # def get_in_scroll_zone(self):
    #     x = self.rect.x - Camera.position[0]
    #     if x < screenWidth * 0.1:
    #         return -1
        
    #     if x > screenWidth * 0.9:
    #         return 1
        
    #     return 0


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        # self.fill((240,240,240))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        # self.right = pygame.image.load(icon/heath.jpg)
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (200, 0, 0), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, (0, 200, 0), (self.x, self.y, self.w*ratio, self.h))

    def get_damage(self, amount):
        if self.hp > 0:
            self.hp -= amount
        if self.hp <= 0:
            alive = False
    def get_health(self, amount):
        if self.hp < self.max_hp:
            self.hp += amount
        if self.hp >= self.max_hp:
            self.hp = self.max_hp


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = snow_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

#create sprite group
bullet_group = pygame.sprite.Group()

PNJ = character('PNJ', 200, 200, 0.5, 5)
yellowPikmin = character('player', 400, 200, 0.7, 5)
health_bar = HealthBar(30, 30, 200, 40, 100)

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

    yellowPikmin.update_animation()
    PNJ.draw()
    yellowPikmin.draw()
    screen_scroll = yellowPikmin.move(moving_left, moving_right)

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    #draw health bar
    health_bar.hp = 50
    health_bar.draw(screen)

    #update player action
    if yellowPikmin.alive:
        if shoot:
            snow_img = Bullet(yellowPikmin.rect.centerx, yellowPikmin.rect.centery, yellowPikmin.direction)
            bullet_group.add(Bullet)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                moving_left = True
            if event.key == pygame.K_t:
                health_bar.get_damage(20)
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_z and yellowPikmin.alive:
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

    pygame.display.update()

pygame.quit()