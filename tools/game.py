from pygame import gfxdraw
import pygame
from Helpers import helpers
from Helpers.helpers import get_token_images
from Models.Point import Point

#<editor-fold desc="GAME SET UP">
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1920,1080), pygame.RESIZABLE)
helpers.loading_screen(screen)

#</editor-fold>

TRANSFORMS = (0.5, 0.55,
              0.6, 0.68,
              0.75,0.82,
              1.0, 1.2)
TRANSFORM_INDEX = TRANSFORMS.index(1.0)
MAX_TRANSFORM_AMOUNT = len(TRANSFORMS) - 1
MIN_TRANSFORM_AMOUNT = 0
TOKEN_SIZE = 0.8

def MAX_X_MARGIN():
    return screen.get_width() / 10

def MAX_Y_MARGIN():
    return MAX_X_MARGIN()
    # return screen.get_height()/10

# load up the images
# game_board_image = pygame.image.load("../data/GOTv2.0.jpg")


OG_BACKGROUND = pygame.image.load("../data/a-game-of-thrones-world-map-westeros-essos.jpg")
# og_background = pygame.Surface.convert(game_board_image)

BACKGROUND_TRANSFORMS = []

for TRANSFORM in TRANSFORMS:
    BACKGROUND_TRANSFORMS.append(pygame.transform.rotozoom(OG_BACKGROUND, 0, TRANSFORM))


territory = pygame.image.load("../data/territory.png")

tokens = get_token_images(TOKEN_SIZE)
placed_tokens = []


# and the surfaces



EDIT_BACKGROUND = OG_BACKGROUND.copy()
BLITTED_BACKGROUND = BACKGROUND_TRANSFORMS[TRANSFORM_INDEX]

CameraX = 0
CameraY = 0

held = False
start_coordinates = None

def holding():
    '''
    Allows the user to move around the map by moving the mouse
    '''
    global CameraX,CameraY,start_coordinates
    coordinates = pygame.mouse.get_pos()

    CameraX += (start_coordinates[0] - coordinates[0])*1.5
    CameraY += (start_coordinates[1] - coordinates[1])*1.5

    start_coordinates = coordinates

def constrain_camera():
    '''
    Keeps the camera from moving away from the game map
    '''
    global CameraX,CameraY
    CameraX = max(CameraX, -MAX_X_MARGIN())
    CameraY = max(CameraY, -MAX_Y_MARGIN())

    CameraX = min(CameraX, BLITTED_BACKGROUND.get_width() - screen.get_width() + MAX_X_MARGIN())
    CameraY = min(CameraY, BLITTED_BACKGROUND.get_height() - screen.get_height() + MAX_Y_MARGIN())


def get_relative_mouse_position_on_map():
    '''
    Returns the mouse position on the map as a percentage of the map
    :return: Point() coordinates
    '''
    coordinates = pygame.mouse.get_pos()
    return ((CameraX + coordinates[0]) / BLITTED_BACKGROUND.get_width(),
            (CameraY + coordinates[1]) / BLITTED_BACKGROUND.get_height())

def turn_relative_into_absolute_position(previous_position):
    return (previous_position[0] * EDIT_BACKGROUND.get_width() - CameraX,
            previous_position[1] * EDIT_BACKGROUND.get_height() - CameraY)


def change_background():
    global BLITTED_BACKGROUND, CameraX, CameraY

    coordinates = pygame.mouse.get_pos()
    pos_relative_to_map = get_relative_mouse_position_on_map()

    BLITTED_BACKGROUND = pygame.transform.rotozoom(EDIT_BACKGROUND, 0, TRANSFORMS[TRANSFORM_INDEX])

    # the mouse was at 0.6 WIDTH when it was at 600 px
    # the mouse is still at 600 px, but we need to set the new ABSOLUTE position to 0.6 WIDTH as well.

    CameraX = pos_relative_to_map[0] * BLITTED_BACKGROUND.get_width() - min(max(coordinates[0], screen.get_width() * 0.25), screen.get_width() * 0.75)
    CameraY = pos_relative_to_map[1] * BLITTED_BACKGROUND.get_height() - min(max(coordinates[1], screen.get_height() * 0.25), screen.get_height() * 0.75)

polygon_points = []

GAME_RUNNING = True


def blit_once(new_pos):
    new_pos = turn_relative_into_absolute_position(new_pos)

    token = tokens[len(placed_tokens) % len(tokens)]

    EDIT_BACKGROUND.blit(token,
                         (new_pos[0] - TOKEN_SIZE * token.get_width() / 2,
                          new_pos[1] - TOKEN_SIZE * token.get_height() / 2))


while GAME_RUNNING:
    clicked = False
    old_transform_index = TRANSFORM_INDEX
    # fill up the screen to prevent multiple images being printed to screen
    screen.fill((50,50,50))

    # check to see if the mouse is being held (so we can move the map around)
    prev_held = held

    if held:
        holding()


    # run through the events
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pass
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            pass


        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.dict['button'] == 2: # MMB pressed
                held = True
                start_coordinates = pygame.mouse.get_pos()
            else:
                clicked = True

                if event.dict['button'] == 1:
                    polygon_points.append(pygame.mouse.get_pos())
                if event.dict['button'] == 3: # right mouse button pressed
                    new_pos = get_relative_mouse_position_on_map()
                    placed_tokens.append(new_pos)
                    blit_once(new_pos)

                if event.dict['button'] == 4: # mouse wheel up
                    TRANSFORM_INDEX += 1
                    TRANSFORM_INDEX = min(TRANSFORM_INDEX,MAX_TRANSFORM_AMOUNT)

                if event.dict['button'] == 5: # mouse wheel down
                    TRANSFORM_INDEX -= 1
                    TRANSFORM_INDEX = max(TRANSFORM_INDEX,MIN_TRANSFORM_AMOUNT)



        if event.type == pygame.MOUSEBUTTONUP:
            if event.dict['button'] == 2: # left mouse button released
                held = False

        # quit the game
        if event.type == pygame.QUIT:
            GAME_RUNNING = False


    # draw the map onto the screen

    # draw rectangles



    # if len(polygon_points) > 2:
    #     # gfxdraw.textured_polygon(BACKGROUND,polygon_points,territory,0,0)
    #     gfxdraw.aapolygon(EDIT_BACKGROUND, polygon_points, (255, 255, 255))
    #     gfxdraw.filled_polygon(EDIT_BACKGROUND,polygon_points,(255,125,125))

    if old_transform_index != TRANSFORM_INDEX or clicked:
        print(TRANSFORM_INDEX)
        change_background()

    constrain_camera()

    screen.blit(BLITTED_BACKGROUND, (0 - CameraX, 0 - CameraY))

    # reconstrain the camera so it doesn't ever leave the map



    pygame.display.flip()
    clock.tick(60)

