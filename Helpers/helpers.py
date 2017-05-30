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

def get_background_transforms(og_background, transforms):
    bg = []

    for transform in transforms:
        bg.append(pygame.transform.rotozoom(og_background, 0, transform))

    return tuple(bg)


def get_onscreen_transforms(background_transforms, flags=0):
    retter = []
    for bg in background_transforms:
        retter.append(pygame.Surface((bg.get_width(),bg.get_height()),flags=flags))

    return tuple(retter)


def MAX_X_MARGIN(screen):
    return screen.get_width() / 10

def MAX_Y_MARGIN(screen):
    return (MAX_X_MARGIN(screen) + screen.get_height()/10) / 2

def constrain_camera(camera, screen, current_background):
    '''
    Keeps the camera from moving away from the game map
    '''

    max_x = MAX_X_MARGIN(screen)
    max_y = MAX_Y_MARGIN(screen)

    camera.x = max(camera.x, -max_x)
    camera.y = max(camera.y, -max_y)

    camera.x = min(camera.x, current_background.get_width() - screen.get_width() + max_x)
    camera.y = min(camera.y, current_background.get_height() - screen.get_height() + max_y)


def get_relative_mouse_position_on_map(camera,current_background):
    '''
    Returns the mouse position on the map as a percentage of the map
    :return: Point() coordinates
    '''
    coordinates = Point(pygame.mouse.get_pos())
    # TODO turn this into a Point return
    return (camera + coordinates).div(Point(current_background.get_size()))
    # return ((camera.x + coordinates[0]) / blitted_background.get_width(),
    #         (camera.y + coordinates[1]) / blitted_background.get_height())

def turn_relative_into_absolute_position(previous_position, current_background):
    return previous_position.mul(Point(current_background.get_size()))
    # return (previous_position[0] * BACKGROUND_TRANSFORMS[transform_index].get_width(),# - camera.x,
    #         previous_position[1] * BACKGROUND_TRANSFORMS[transform_index].get_height())# - camera.y)

