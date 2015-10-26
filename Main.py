from Cursor import Cursor
from Level import Level
import pygame


def main():

    pygame.init

    running = True
    size = (1920, 1080)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    level = Level(10)

    cursor = Cursor()

    pygame.mouse.set_visible(False)

    background = pygame.image.load("resources/images/background.png").convert()


    def shoot():
        pos = pygame.mouse.get_pos()
        level.shoot(pos[0], pos[1])


    """ Game Loop """
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



        level.update()
        cursor.update()

        """ Draws """
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        level.draw(screen)
        cursor.draw(screen)


        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 30 frames per second
        clock.tick(30)



    pygame.quit()

if __name__ == "__main__":
    main()
