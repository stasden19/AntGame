import time
import pygame
import screen
import game
import constants as c
import numpy as np

root = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption('AntGame')
clock = pygame.time.Clock()
root.fill(c.COLOR_BLACK)
pygame.display.update()
antgame = game.AntGame(root)
antgame.start()
anthill = antgame.create_anthill(30, 30)
all_walls = []
run = True
all_ants = [game.Ant(root, anthill.xcor, anthill.ycor) for _ in range(c.ANT_COUNT)]
all_food = []
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == c.WALL_FILL:
                pos = pygame.mouse.get_pos()
                adding_wall = antgame.create_wall(pos[0], pos[1])
                if adding_wall not in all_walls:
                    all_walls.append(adding_wall)
            elif event.key == c.FOOD_FILL:
                pos = pygame.mouse.get_pos()
                adding = antgame.create_food(pos[0], pos[1])
                if adding not in all_food:
                    all_food.append(adding)

    for i in range(len(all_ants)):
        all_ants[i].step()
        if all_walls:
            all_ants[i].check_wall(all_walls)
    pygame.display.update()
    clock.tick(40)
pygame.quit()
