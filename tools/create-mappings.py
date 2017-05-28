import pygame
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1920,1080))

max_y_margin = 108
max_x_margin = 192

# load up the images
game_board_image = pygame.image.load("../data/GOTv2.0.jpg")

# Load the image
move_tokens = pygame.image.load("../data/Order Tokens.png")

width, height = move_tokens.get_width() / 5, move_tokens.get_height()

tokens = [(i*width, 0, width, height) for i in range(0,5)]



placed_tokens = []


# and the surfaces
og_background = pygame.Surface.convert(game_board_image)
half_background = pygame.transform.rotozoom(og_background, 0, 0.5)
TRANSFORM_AMOUNT = 1
BACKGROUND = og_background

CameraX = 0
CameraY = 0

held = False
start_coordinates = None


def holding():
    global CameraX,CameraY,start_coordinates
    coordinates = pygame.mouse.get_pos()

    CameraX += (start_coordinates[0] - coordinates[0])*1.5
    CameraY += (start_coordinates[1] - coordinates[1])*1.5

    start_coordinates = coordinates

def constrain_camera():
    global CameraX,CameraY
    CameraX = max(CameraX,-max_x_margin)
    CameraY = max(CameraY,-max_y_margin)

    CameraX = min(CameraX, BACKGROUND.get_width() - screen.get_width() + max_x_margin)
    CameraY = min(CameraY, BACKGROUND.get_height() - screen.get_height() + max_y_margin)


def get_relative_mouse_position_on_map():
    coordinates = pygame.mouse.get_pos()
    return ((CameraX + coordinates[0])/BACKGROUND.get_width(),
            (CameraY + coordinates[1])/BACKGROUND.get_height())

def turn_relative_into_absolute_position(previous_position):
    return (previous_position[0] * BACKGROUND.get_width() - CameraX,
            previous_position[1] * BACKGROUND.get_height() - CameraY)


def change_background(background):
    global BACKGROUND, CameraX, CameraY

    coordinates = pygame.mouse.get_pos()
    pos_relative_to_map = get_relative_mouse_position_on_map()

    # pos_relative_to_screen = (coordinates[0] / screen.get_width(), coordinates[1] / screen.get_height())

    # x = CameraX # basically pretend that this is where the camera is located along the map
    # y = CameraY # basically pretend that this is where the camera is located along the map

    BACKGROUND = background

    # the mouse was at 0.6 WIDTH when it was at 600 px
    # the mouse is still at 600 px, but we need to set the new ABSOLUTE position to 0.6 WIDTH as well.

    CameraX = pos_relative_to_map[0] * BACKGROUND.get_width() - min(max(coordinates[0], screen.get_width()*0.25),screen.get_width()*0.75)
    CameraY = pos_relative_to_map[1] * BACKGROUND.get_height() - min(max(coordinates[1], screen.get_height()*0.25),screen.get_height()*0.75)


GAME_RUNNING = True
while GAME_RUNNING:
    # fill up the screen to prevent multiple images being printed to screen
    screen.fill((0,0,0))

    # check to see if the mouse is being held (so we can move the map around)
    if held:
        holding()


    # run through the events
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.dict['button'] == 1: # left mouse button pressed
                held = True
                start_coordinates = pygame.mouse.get_pos()
            elif event.dict['button'] == 3: # right mouse button pressed
                placed_tokens.append(get_relative_mouse_position_on_map())
            elif event.dict['button'] == 4: # mouse wheel up
                if BACKGROUND is not og_background:
                    TRANSFORM_AMOUNT = 1
                    change_background(og_background)
            elif event.dict['button'] == 5: # mouse wheel down
                if BACKGROUND is not half_background:
                    TRANSFORM_AMOUNT = 0.5
                    change_background(half_background)


        if event.type == pygame.MOUSEBUTTONUP:
            if event.dict['button'] == 1: # left mouse button released
                held = False
            elif event.dict['button'] == 5:
                pass
            elif event.dict['button'] == 4:
                pass


        if event.type == pygame.QUIT:
            GAME_RUNNING = False


    # reconstrain the camera so it doesn't ever leave the map
    constrain_camera()

    # draw the map onto the screen
    screen.blit(BACKGROUND, (0 - CameraX, 0 - CameraY))

    # draw rectangles

    for i in range(0, len(placed_tokens)):
        rectum = placed_tokens[i]
        new_pos = turn_relative_into_absolute_position(rectum)
        # pygame.draw.rect(screen, (255, 0, 255), (new_pos[0] - 40*TRANSFORM_AMOUNT, new_pos[1] - 40*TRANSFORM_AMOUNT, 80*TRANSFORM_AMOUNT, 80*TRANSFORM_AMOUNT))

        # Blit second half
        screen.blit(move_tokens, new_pos, tokens[i % 5])


    # refresh screen
    pygame.display.flip()
    clock.tick(60)
