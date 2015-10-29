from enum import Enum
from Cursor import Cursor
from Level import Level
import pygame


class GameState(Enum):
    mainmenu = 0
    running = 1


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
    gamestate = GameState.running



    def shoot():
        pos = cursor.getXY()
        level.shoot(pos[0], pos[1])
        cursor.shoot()


    """ Game Loop """
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #shoot()
                    level.decrease_health(100)
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot()



        level.update()
        cursor.update()

        """ Draws """
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

        if GameState.mainmenu == gamestate:
            pass
        elif GameState.running == gamestate:
            level.draw(screen)
            pass

        cursor.draw(screen)


        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 30 frames per second
        clock.tick(30)



    pygame.quit()

if __name__ == "__main__":
    main()
