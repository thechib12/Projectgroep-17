from Cursor import Cursor

__author__ = 'reneb_000'
import pygame

pygame.init

running = True
size = (700, 500)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1900, 1080), pygame.FULLSCREEN)

cursor_x = 200
cursor_y = 200
cursor_color = (0, 0, 0)

cursor = Cursor()
#all sprites classes need to be added to allSprites. This object will draw all the objects
allSprites = pygame.sprite.Group()
allSprites.add(cursor)

pygame.mouse.set_visible(False)


def cursor_set_cords(x, y):
    global cursor_x
    global cursor_y
    cursor_x = x
    cursor_y = y


def draw_curs(screen_arg, x, y, width, color):
    pygame.draw.line(screen_arg, color, [x - width, y], [x + width, y], 5)
    pygame.draw.line(screen_arg, color, [x, y - width], [x, y + width], 5)


def shoot():
    print("SHOT")
    pass


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot()
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot()


    # --- Game logic should go here

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill((255, 255, 255))

    allSprites.update()
    allSprites.draw(screen)


    #cursor_set_cords(pos[0], pos[1])
    #draw_curs(screen, cursor_x, cursor_y, 50, cursor_color)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(30)

pygame.quit()

