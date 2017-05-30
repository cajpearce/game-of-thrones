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
TRANSFORM_AMOUNTS = (0.5, 0.64, 0.8,
                     1.0, 1.25)

MAX_TRANSFORM_AMOUNT = len(TRANSFORM_AMOUNTS) - 1
MIN_TRANSFORM_AMOUNT = 0
TOKEN_SIZE = 0.5


OG_BACKGROUND = pygame.image.load("../data/low_detail.jpg")

# will take a while ...

TOKEN_IMAGES = helpers.get_token_images(TOKEN_SIZE)
CHOSEN_TOKEN_IMAGES = helpers.get_token_images(TOKEN_SIZE*4)
# ONSCREEN_TRANSFORMS =  helpers.get_onscreen_transforms(Background.TRANSFORMS, flags=pygame.SRCALPHA)
#</editor-fold>


class TransformLevel:
    # todo rename this

    def __init__(self, transform_index):
        self.transform_index = transform_index
        self.transform_amount = TRANSFORM_AMOUNTS[transform_index]

        self.background = Background(transform_index)
        self.onscreen = Onscreen(transform_index)
        self.tokens = Token(self.transform_amount).images # todo is this the way I want to go forward?


class Background:
    TRANSFORMS = helpers.get_background_transforms(OG_BACKGROUND,TRANSFORM_AMOUNTS)

class Onscreen:
    TRANSFORMS = helpers.get_onscreen_transforms(Background.TRANSFORMS, flags=pygame.SRCALPHA)

    @staticmethod
    def blit_to_all(new_pos):
        for i in range(len(Onscreen.TRANSFORMS)):
            temp_pos = helpers.turn_relative_into_absolute_position(new_pos, Background.TRANSFORMS[i])

            token = TOKEN_IMAGES[current_token_used]

            Onscreen.TRANSFORMS[i].blit(token,
                                        (temp_pos.x - token.get_width() / 2,
                                         temp_pos.y - token.get_height() / 2))


class Token:
    TOKEN_SIZE = 0.5
    def __init__(self, modifier=1):
        self.images = helpers.get_token_images(modifier*TOKEN_SIZE)


transform_index = TRANSFORM_AMOUNTS.index(1.0)
placed_tokens = []
current_token_used = 0
def change_token(key):
    global current_token_used
    current_token_used = abs(pygame.K_1 - key)


edit_background = OG_BACKGROUND.copy()

edit_onscreen = pygame.Surface((OG_BACKGROUND.get_width(),OG_BACKGROUND.get_height()),flags=pygame.SRCALPHA)
blitted_background = Background.TRANSFORMS[transform_index]

camera = Point((0,0))

held = False
start_coordinates = None

def move_camera_when_holding_mmb(camera):
    '''
    Allows the user to move around the map by moving the mouse
    '''
    global start_coordinates
    coordinates = Point(pygame.mouse.get_pos())

    camera.x += (start_coordinates.x - coordinates.x)*1.5
    camera.y += (start_coordinates.y - coordinates.y)*1.5

    start_coordinates = coordinates

def change_background(camera):
    global blitted_background

    coordinates = Point(pygame.mouse.get_pos())
    pos_relative_to_map = helpers.get_relative_mouse_position_on_map(camera, blitted_background)

    blitted_background = Background.TRANSFORMS[transform_index]

    # the mouse was at 0.6 WIDTH when it was at 600 px
    # the mouse is still at 600 px, but we need to set the new ABSOLUTE position to 0.6 WIDTH as well.

    camera.x = pos_relative_to_map.x * blitted_background.get_width() - coordinates.x
    camera.y = pos_relative_to_map.y * blitted_background.get_height() - coordinates.y

polygon_points = []






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
            move_camera_when_holding_mmb(camera)
            helpers.constrain_camera(camera, screen, blitted_background)

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
                    start_coordinates = Point(pygame.mouse.get_pos())
                else:
                    reblit = True
                    clicked = True

                    if event.dict['button'] == 1:
                        polygon_points.append(pygame.mouse.get_pos())
                    if event.dict['button'] == 3:  # right mouse button pressed
                        new_pos = helpers.get_relative_mouse_position_on_map(camera, blitted_background)
                        placed_tokens.append(new_pos)
                        Onscreen.blit_to_all(new_pos)

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
                helpers.constrain_camera(camera, screen, blitted_background)

        if reblit or blit_first_time:

            blit_first_time = False

            screen.fill((50, 50, 50))

            screen.blit(blitted_background, camera.get(neg=True))
            screen.blit(Onscreen.TRANSFORMS[transform_index], camera.get(neg=True))

            display_token = CHOSEN_TOKEN_IMAGES[current_token_used]

            screen.blit(display_token, (32, screen.get_height() - display_token.get_height() - 32))
            pygame.display.flip()
        # clock.tick(60)
        # plot the background to the screen


# main()
import cProfile as profile

profile.run('main()')
