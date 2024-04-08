import pygame
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
        
        self.surf = pygame.Surface((80, 80))
        self.rect = self.surf.get_rect()
   
        self.pos = BaseWindow().vec((1920/2, 1080/2))
        self.vel = BaseWindow().vec(0,0)
        self.acc = BaseWindow().vec(0,0)

        self.fric = BaseWindow().FRIC

    def move(self):
        self.acc = BaseWindow().vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_s]:
            self.slide()
        else:
            if pressed_keys[K_q]:
                self.acc.x = -BaseWindow().ACC
                self.direction = 0
            if pressed_keys[K_d]:
                self.acc.x = BaseWindow().ACC
                self.direction = 1
             
        self.acc.x += self.vel.x * self.fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > BaseWindow().wid:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = BaseWindow().wid
            
        self.rect.midbottom = self.pos
        self.fric = BaseWindow().FRIC

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
        if hits:
            self.vel.x += 30 * (1 if self.vel.x >= -0.01 else -1)
    
    def slide(self):
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if hits:
            self.fric = -0.009

class snowball:
    def __init__(self, x, y, targetx, targety):
        self.speed = 20
    
        self.surf = pygame.Surface((20,20))
        self.rect = self.surf.get_rect()

        self.rect.midbottom = P1.rect.midbottom
        self.point = pygame.mouse.get_pos()

        self.angle = math.atan2(targety-y, targetx-x) 

        self.dir = BaseWindow().vec(math.cos(self.angle)*self.speed,math.sin(self.angle)*self.speed)
        self.acc = BaseWindow().vec(0,0)
        self.vel = self.dir
        self.pos = BaseWindow().vec((x, y))

    def move(self):
        self.acc = BaseWindow().vec(0,0.3)
        

        self.acc.x += self.vel.x * -0.001
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        self.rect.center = self.pos

class Niveau(pygame.sprite.Sprite):
    def __init__(self, gameDisplay):
        super().__init__()
        self.coords = open("level0_data.csv", "r", encoding='utf-8')
        self.length = 0
        self.tab = []
        self.tab_area = []
        self.image = pygame.transform.scale(pygame.image.load(r'sol.jpg'), (100, 100))
        self.gameDisplay = gameDisplay
        self.flip =  False
        self.rect = self.image.get_rect()
        
        
        for x in open("level0_data.csv"):
            self.length += 1
            y = x.split(",")

            self.tab.append(y)

        for i in range(self.length):
            for j in range(30):
                if self.tab[i][j] == "0":
                    self.gameDisplay.blit(self.image, (500,500))
                    print("a")

    def draw(self):
        self.gameDisplay.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

                    

class platform(pygame.sprite.Sprite): # PAS TOUCHE
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((BaseWindow().wid, 20))
        self.surf.fill((100,100,100))
        self.rect = self.surf.get_rect(center = (BaseWindow().wid/2, BaseWindow().hei - 10))
 
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
    s = []

    
    n = Niveau(gameDisplay)

    while running:

        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(bg, (0, 0))
        Player().player(playerX, playerY)
        
        for event in pygame.event.get():
################### PLAYER MOVEMENT
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o]:
                pygame.QUIT
                running = False
            if keys[pygame.K_SPACE]:
                P1.jump()
            
            if keys[pygame.K_LSHIFT]:
                now = pygame.time.get_ticks()
                if now - lastdash >= cooldowndash and -10 < P1.vel.x < 10:
                    lastdash = now
                    playerIMG = pygame.transform.rotate(playerIMG, -90)
                    sliding = True
                    P1.dash()
            now = pygame.time.get_ticks()
            if now - lastdash >= (cooldowndash //30)  and sliding:
                playerIMG = pygame.transform.rotate(playerIMG, 90)
                sliding = False

        P1.move()
        P1.update()
        
        gameDisplay.blit(playerIMG, P1.rect)
        gameDisplay.blit(PT1.surf, PT1.rect)
        n.draw()

        for entity in s:

            gameDisplay.blit(snowballimg, entity.rect)
            entity.move()

        pygame.display.update() 
        clock.tick(BaseWindow().fps)
    #####################

PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

bg, playerIMG, snowballimg = setup_imgs(BaseWindow().wid, BaseWindow().hei)
gameDisplay = gd(BaseWindow().wid, BaseWindow().hei)

gameDisplay.blit(bg, (0, 0))

play(gameDisplay, playerIMG)

pygame.quit()
