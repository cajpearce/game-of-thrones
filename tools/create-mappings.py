import pygame
ORANGE = (255,155,0)
RED = (255,0,0)
pygame.init()
screen = pygame.display.set_mode((1920,1080))
done = False

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
    global held,CameraX,CameraY,start_coordinates
    if held:
        coordinates = pygame.mouse.get_pos()

        CameraX += (start_coordinates[0] - coordinates[0])*1.5
        CameraY += (start_coordinates[1] - coordinates[1])*1.5

        start_coordinates = coordinates

while not done:
    screen.fill((0,0,0))

    if held:
        holding()


    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.dict['button'] == 1: # left mouse button pressed
                held = True
                start_coordinates = pygame.mouse.get_pos()
            elif event.dict['button'] == 4: # mouse wheel up
                current_background_image = og_background
                # image_used = pygame.transform.rotozoom(background_image,0,transform_amount)
            elif event.dict['button'] == 5: # mouse wheel down
                current_background_image = half_background
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
