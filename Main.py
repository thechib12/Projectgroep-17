from Cursor import Cursor
import Zombie

__author__ = 'reneb_000'
import pygame

pygame.init

running = True
size = (800, 600)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1900, 1080), pygame.FULLSCREEN)

cursor_x = 200
cursor_y = 200
cursor_color = (0, 0, 0)

cursor = Cursor()
#all sprites classes need to be added to allSprites. This object will draw all the objects
allSprites = pygame.sprite.Group()
allSprites.add(cursor)
#original zombie is 660 px heigh
for i in range(1,10):
    zombie = Zombie.Zombie(198, i*198)
    allSprites.add(zombie)




zombie = Zombie.Zombie(198, 0)
allSprites.add(zombie)

pygame.mouse.set_visible(False)




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




    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 30 frames per second
    clock.tick(30)

pygame.quit()

