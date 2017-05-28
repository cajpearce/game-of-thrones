import pygame
ORANGE = (255,155,0)
RED = (255,0,0)
pygame.init()
screen = pygame.display.set_mode((1920,1080))
done = False

toggle_color = True
color = ORANGE
while not done:
    if toggle_color:
        color = RED
    else:
        color = ORANGE

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            toggle_color = not toggle_color

        if event.type == pygame.QUIT:
            done = True
    # events


    pygame.draw.rect(screen,color, pygame.Rect(30,30,60,60))

    # refresh screen

    pygame.display.flip()


class AreaBox:
    def __init__(self,name, island_id, color):
        self.name = name
        self.island_id = island_id
        

    def draw(self, screen):
        pygame.draw.rect(screen,