import pygame
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1920,1080))
done = False
max_y_margin = 108
max_x_margin = 192

# load up the images
game_board_image = pygame.image.load("../data/GOTv2.0.jpg")

# and the surfaces
og_background = pygame.Surface.convert(game_board_image)
half_background = pygame.transform.rotozoom(og_background, 0, 0.5)
current_background_image = og_background

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

    print(screen.get_width())
    CameraX = min(CameraX,current_background_image.get_width() - screen.get_width() + max_x_margin)
    CameraY = min(CameraY,current_background_image.get_height() - screen.get_height() + max_y_margin)

while not done:
    screen.fill((0,0,0))

    if held:
        holding()
        constrain_camera()


    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.dict['button'] == 1: # left mouse button pressed
                held = True
                start_coordinates = pygame.mouse.get_pos()
            elif event.dict['button'] == 4: # mouse wheel up
                current_background_image = og_background
                constrain_camera()
                # image_used = pygame.transform.rotozoom(background_image,0,transform_amount)
            elif event.dict['button'] == 5: # mouse wheel down
                current_background_image = half_background
                constrain_camera()
                # transform_amount -= 0.05
                # image_used = pygame.transform.rotozoom(background_image,0,transform_amount)


        if event.type == pygame.MOUSEBUTTONUP:
            if event.dict['button'] == 1: # left mouse button released
                held = False
            elif event.dict['button'] == 5:
                pass
            elif event.dict['button'] == 4:
                pass


        if event.type == pygame.QUIT:
            done = True
    # events


    screen.blit(current_background_image, (0 - CameraX, 0 - CameraY))

    # refresh screen

    pygame.display.flip()
    clock.tick(60)
