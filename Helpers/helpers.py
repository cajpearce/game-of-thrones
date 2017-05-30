import pygame

from Models.Point import Point


def loading_screen(screen):
    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.SysFont("timesnewroman", 48, True)
    # render text
    label = myfont.render("Game of Lollys Stokeworth (c)", 1, (255, 255, 255))
    center_of_label = label.get_rect().center
    screen_center = screen.get_rect().center
    loc = Point(screen_center) - Point(center_of_label)
    screen.blit(label, loc.get())
    pygame.display.flip()