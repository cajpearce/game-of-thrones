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


def get_token_images(token_size):
    # Load the image
    master_move_tokens_image = pygame.image.load("../data/Order Tokens.png")
    master_move_tokens_image = pygame.transform.rotozoom(master_move_tokens_image, 0, token_size)
    width, height = master_move_tokens_image.get_width() / 5, master_move_tokens_image.get_height()
    tokens = []
    for i in range(5):
        tokens.append(master_move_tokens_image.subsurface(pygame.Rect((i * width, 0, width, height))))

    return tuple(tokens)
