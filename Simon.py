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
scroll_thresh = 200
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

def draw_bg():
    screen.fill(BG)
    screen.blit(bg_img, (0,0))


class character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = True
        self.animation_list =[]
        img = pygame.image.load(f'{self.char_type}').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        #reset movement variables
        screen_scroll = 0
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
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll on player position
        if self.char_type == 'player':
            if self.rect.right > screenWidth - scroll_thresh or self.rect.left < scroll_thresh:
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

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

bluepikmin = character('bluepikmin.png', 200, 200, 0.1, 5)
yellowPikmin = character('yellowpikmin.png', 400, 200, 0.1, 5)

run = True

while run:

    clock.tick(FPS)

    draw_bg()
    
    bluepikmin.draw()
    yellowPikmin.draw()
    screen_scroll = yellowPikmin.move(moving_left, moving_right)

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    print(screen_scroll)

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
            if event.key == pygame.K_d:
                moving_right = True
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