from enum import Enum
import threading
from Cursor import Cursor
from GameState import *

from Level import Level, Popup, PopupType
import pygame
from ShopEntry import Shop

pygame.init

running = True
size = (1920, 1080)
clock = pygame.time.Clock()

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


lock = threading.Lock()
cursor = Cursor(lock)
cursor.start()

pygame.mouse.set_visible(False)

"""" MENU """""


background = pygame.image.load("resources/images/background.png").convert()
gamestate = GameState(GameStateEnum.mainmenu)
level = Level(10, gamestate)
popup = Popup(PopupType.mainmenu, level, gamestate)
shop = Shop(cursor, gamestate)


def shoot():
    pos = cursor.getXY()
    if GameStateEnum.mainmenu == gamestate.getState():
        popup.click(pos[0], pos[1])
    elif GameStateEnum.running == gamestate.getState():
        level.shoot(pos[0], pos[1])
    elif GameStateEnum.shop == gamestate.getState():
        shop.click(pos[0], pos[1])
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


    cursor.update()

    """ Clear and background """
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    if GameStateEnum.mainmenu == gamestate.getState():
        """ Update """

        """ Draw """
        popup.draw(screen)
        pass
    elif GameStateEnum.running == gamestate.getState():
        """ Update """
        level.update()

        """ Draw """
        level.draw(screen)
        pass
    elif GameStateEnum.shop == gamestate.getState():
        """ Upfdate """

        """ Draw """
        shop.draw(screen)

    cursor.draw(screen)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 30 frames per second
    clock.tick(30)

pygame.quit()


def set_game_state(state):
    global gamestate
    gamestate = state

