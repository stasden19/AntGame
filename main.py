import math
import time
import pygame
import game
import constants as c

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
    root.fill(c.COLOR_BLACK)
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
                    all_food.append(game.Food(*adding))
    for i in range(len(all_food)):
        all_food[i].draw(root)
    for i in range(len(all_ants)):
        all_ants[i].step()
        all_ants[i].draw()
        all_ants[i].draw_fer()
        # if all_ants[i].step_counter % 1 == 0:
        coords = all_ants[i].find_colors_in_radius(root)
        for coord in coords:
            if 'food' in coord:
                x_food = (coord['food'][0] + coord['food'][0] + c.RECT_SIDE) // 2
                y_food = (coord['food'][1] + coord['food'][1] + c.RECT_SIDE) // 2
                ant_x = all_ants[i].xcor
                ant_y = all_ants[i].ycor
                all_ants[i].direction = int(math.atan(abs(ant_y - y_food) / abs(ant_x - x_food)))
                break
        if all_walls:
            all_ants[i].check_wall(all_walls)

    for i in all_walls:
        pygame.draw.rect(
            root,
            c.WALL_COLOR,
            pygame.rect.Rect((i[0] // c.RECT_SIDE * c.RECT_SIDE, i[1] // c.RECT_SIDE * c.RECT_SIDE),
                             (c.RECT_SIDE, c.RECT_SIDE), width=0),
            width=0
        )
    pygame.display.update()
    clock.tick(10)
pygame.quit()