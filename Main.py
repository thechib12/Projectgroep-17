from Cursor import Cursor
from Level import Level
import Zombie
import pygame


def main():

    pygame.init

    running = True
    size = (1366, 768)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    # load all images
    zombie_sheet_normal = pygame.image.load("resources/images/enemies/zombie3.png")
    zombie_sheet_one_leg = pygame.image.load("resources/images/enemies/one_leg.png")
    zombie_sheet_no_leg = pygame.image.load("resources/images/enemies/no_leg.png")

    level = Level(10)
    fontSize = 50
    textColor = (0, 0, 0)
    font = pygame.font.init()
    font = pygame.font.Font("resources/fonts/Lato-Regular.ttf", fontSize)
    level_remaining = level.getRemaining()
    texttest = font.render("Remaining: " + str(level_remaining), True, textColor)

    cursor = Cursor()
    # all sprites classes need to be added to allSprites. This object will draw all the objects
    allSprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    # allSprites.add(cursor)
    # original zombie is 660 px height
    """
    for i in range(0, 5):
        zombie = Zombie.Zombie(zombie_sheet_normal, zombie_sheet_one_leg, zombie_sheet_no_leg, i*198)
        allSprites.add(zombie)
        enemies.add(zombie)
    """


    pygame.mouse.set_visible(False)



    def shoot():
        for enemy in enemies:
            pos = pygame.mouse.get_pos()
            if enemy.hit(pos[0], pos[1]):
                removeSprite(enemy)
        pass


    def removeSprite(spriteobject):
        allSprites.remove(spriteobject)
        enemies.remove(spriteobject)

    def addZombie(y):
        zombie = Zombie.Zombie(zombie_sheet_normal, zombie_sheet_one_leg, zombie_sheet_no_leg, y)
        allSprites.add(zombie)
        enemies.add(zombie)

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


        """ Updates """
        returnVal = level.update()
        if returnVal > 0:
            addZombie(returnVal)
        if level_remaining != level.getRemaining():
            texttest = font.render("Remaining: " + str(level.getRemaining()), fontSize, textColor)
        allSprites.update()
        cursor.update()

        """ Draws """
        screen.fill((255, 255, 255))
        screen.blit(texttest, (0, 0))
        allSprites.draw(screen)
        cursor.draw(screen)





        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 30 frames per second
        clock.tick(30)




    pygame.quit()

if __name__ == "__main__":
    main()
