import pygame, sys

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


pygame.init()
clock = pygame.time.Clock()

black = (0, 0, 0)
green = (0, 0, 255)

width = 640
height = 480

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FPS Test")

font = pygame.font.Font(None, 36)

fps_counter = FPSCounter(screen, font, clock, green, (150, 10))

while True:
    screen.fill(black)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    fps_counter.render()
    fps_counter.update()

    pygame.display.update()
    
    clock.tick(60)