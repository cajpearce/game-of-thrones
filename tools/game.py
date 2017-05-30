from pygame import gfxdraw
import pygame
from Helpers import helpers
from Models.Point import Point

#<editor-fold desc="GAME SET UP">
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1920,1080), pygame.RESIZABLE)
helpers.loading_screen(screen)

#</editor-fold>


#<editor-fold desc="CONSTANTS">
TRANSFORMS = (0.5,0.64,0.8,
              1.0, 1.25)

MAX_TRANSFORM_AMOUNT = len(TRANSFORMS) - 1
MIN_TRANSFORM_AMOUNT = 0
TOKEN_SIZE = 0.5

def MAX_X_MARGIN():
    return screen.get_width() / 10

def MAX_Y_MARGIN():
    return (MAX_X_MARGIN() + screen.get_height()/10) / 2

OG_BACKGROUND = pygame.image.load("../data/low_detail.jpg")

# will take a while ...
BACKGROUND_TRANSFORMS = helpers.get_background_transforms(OG_BACKGROUND,TRANSFORMS)
TOKEN_IMAGES = helpers.get_token_images(TOKEN_SIZE)
CHOSEN_TOKEN_IMAGES = helpers.get_token_images(TOKEN_SIZE*4)
ONSCREEN_TRANSFORMS =  helpers.get_onscreen_transforms(BACKGROUND_TRANSFORMS, flags=pygame.SRCALPHA)
#</editor-fold>


transform_index = TRANSFORMS.index(1.0)
placed_tokens = []
current_token_used = 0
def change_token(key):
    global current_token_used
    current_token_used = abs(pygame.K_1 - key)


edit_background = OG_BACKGROUND.copy()

edit_onscreen = pygame.Surface((OG_BACKGROUND.get_width(),OG_BACKGROUND.get_height()),flags=pygame.SRCALPHA)
blitted_background = BACKGROUND_TRANSFORMS[transform_index]

camera = Point((0,0))

held = False
start_coordinates = None

def holding(camera):
    '''
    Allows the user to move around the map by moving the mouse
    '''
    global start_coordinates
    coordinates = pygame.mouse.get_pos()

    # camera += (Point(start_coordinates) - Point(coordinates))*1.5
    camera.x += (start_coordinates[0] - coordinates[0])*1.5
    camera.y += (start_coordinates[1] - coordinates[1])*1.5

    start_coordinates = coordinates

def constrain_camera(camera):
    '''
    Keeps the camera from moving away from the game map
    '''
    camera.x = max(camera.x, -MAX_X_MARGIN())
    camera.y = max(camera.y, -MAX_Y_MARGIN())

    camera.x = min(camera.x, blitted_background.get_width() - screen.get_width() + MAX_X_MARGIN())
    camera.y = min(camera.y, blitted_background.get_height() - screen.get_height() + MAX_Y_MARGIN())


def get_relative_mouse_position_on_map():
    '''
    Returns the mouse position on the map as a percentage of the map
    :return: Point() coordinates
    '''
    coordinates = pygame.mouse.get_pos()
    return ((camera.x + coordinates[0]) / blitted_background.get_width(),
            (camera.y + coordinates[1]) / blitted_background.get_height())

def turn_relative_into_absolute_position(previous_position, transform_index):

    return (previous_position[0] * BACKGROUND_TRANSFORMS[transform_index].get_width(),# - camera.x,
            previous_position[1] * BACKGROUND_TRANSFORMS[transform_index].get_height())# - camera.y)


def change_background(camera):
    global blitted_background

    coordinates = pygame.mouse.get_pos()
    pos_relative_to_map = get_relative_mouse_position_on_map()

    blitted_background = BACKGROUND_TRANSFORMS[transform_index]

    # the mouse was at 0.6 WIDTH when it was at 600 px
    # the mouse is still at 600 px, but we need to set the new ABSOLUTE position to 0.6 WIDTH as well.

    camera.x = pos_relative_to_map[0] * blitted_background.get_width() - min(max(coordinates[0], screen.get_width() * 0.25), screen.get_width() * 0.75)
    camera.y = pos_relative_to_map[1] * blitted_background.get_height() - min(max(coordinates[1], screen.get_height() * 0.25), screen.get_height() * 0.75)

polygon_points = []



def blit_to_all(new_pos):
    for i in range(len(TRANSFORMS)):
        temp_pos = turn_relative_into_absolute_position(new_pos, i)

        token = TOKEN_IMAGES[current_token_used]

        ONSCREEN_TRANSFORMS[i].blit(token,
                             (temp_pos[0] - token.get_width() / 2,
                              temp_pos[1] - token.get_height() / 2))


def main():
    global screen, held, start_coordinates, transform_index, camera
    pygame.event.clear()
    GAME_RUNNING = True
    blit_first_time = True

    while GAME_RUNNING:
        event = pygame.event.wait()
        clicked = False
        reblit = False
        old_transform_index = transform_index
        # fill up the screen to prevent multiple images being printed to screen

        # check to see if the mouse is being held (so we can move the map around)
        prev_held = held

        if held:
            reblit = True
            holding(camera)
            constrain_camera(camera)

        # run through the events

        # for event in pygame.event.get():
        if True:
            if event.type == pygame.VIDEORESIZE:
                reblit = True
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


            if event.type == pygame.KEYDOWN:
                reblit = True
                if event.key >= pygame.K_1 and event.key <= pygame.K_5:
                    change_token(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.dict['button'] == 2:  # MMB pressed
                    held = True
                    start_coordinates = pygame.mouse.get_pos()
                else:
                    reblit = True
                    clicked = True

                    if event.dict['button'] == 1:
                        polygon_points.append(pygame.mouse.get_pos())
                    if event.dict['button'] == 3:  # right mouse button pressed
                        new_pos = get_relative_mouse_position_on_map()
                        placed_tokens.append(new_pos)
                        blit_to_all(new_pos)

                    if event.dict['button'] == 4:  # mouse wheel up
                        transform_index += 1
                        transform_index = min(transform_index, MAX_TRANSFORM_AMOUNT)

                    if event.dict['button'] == 5:  # mouse wheel down
                        transform_index -= 1
                        transform_index = max(transform_index, MIN_TRANSFORM_AMOUNT)

            if event.type == pygame.MOUSEBUTTONUP:

                if event.dict['button'] == 2:  # left mouse button released
                    reblit = True
                    held = False

            # quit the game
            if event.type == pygame.QUIT:
                GAME_RUNNING = False

            # if len(polygon_points) > 2:
            #     gfxdraw.aapolygon(EDIT_BACKGROUND, polygon_points, (255, 255, 255))
            #     gfxdraw.filled_polygon(EDIT_BACKGROUND,polygon_points,(255,125,125))

            if old_transform_index != transform_index:
                change_background(camera)
                constrain_camera(camera)

        if reblit or blit_first_time:

            blit_first_time = False

            screen.fill((50, 50, 50))

            screen.blit(blitted_background, camera.get(neg=True))
            screen.blit(ONSCREEN_TRANSFORMS[transform_index], camera.get(neg=True))

            display_token = CHOSEN_TOKEN_IMAGES[current_token_used]

            screen.blit(display_token, (32, screen.get_height() - display_token.get_height() - 32))
            pygame.display.flip()
        # clock.tick(60)
        # plot the background to the screen


# main()
import cProfile as profile

profile.run('main()')