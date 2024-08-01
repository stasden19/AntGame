import math
import random
import pygame
import constants as c
from math import cos, radians, sin


class Anthill:
    def __init__(self, xcor, ycor):
        self.color = c.COLOR_ANTHILL
        self.xcor = xcor
        self.ycor = ycor

    def draw(self, scr):
        pygame.draw.rect(
            scr,
            self.color,
            pygame.rect.Rect((self.xcor // c.RECT_SIDE * c.RECT_SIDE, self.ycor // c.RECT_SIDE * c.RECT_SIDE),
                             (c.RECT_SIDE, c.RECT_SIDE), width=1),
            width=0
        )


class AntGame:
    def __init__(self, scr: pygame.Surface):
        self.scr = scr  # экран на котором все отображается

    def start(self):
        pass
        # for i in range(c.SCREEN_WIDTH // c.RECT_SIDE):
        #     for j in range(c.SCREEN_HEIGHT // c.RECT_SIDE):
        #         pygame.draw.rect(
        #             self.scr,
        #             c.BORDER_COLOR,
        #             pygame.rect.Rect((i * c.RECT_SIDE, j * c.RECT_SIDE), (c.RECT_SIDE, c.RECT_SIDE), width=1),
        #             width=1
        #         )
        # pygame.display.update()

    @staticmethod
    def drawrect_cords(self, x, y, color, width=0):
        pygame.draw.rect(
            self.scr,
            color,
            pygame.rect.Rect((x // c.RECT_SIDE * c.RECT_SIDE, y // c.RECT_SIDE * c.RECT_SIDE),
                             (c.RECT_SIDE, c.RECT_SIDE), width=1),
            width=width
        )
        # pygame.display.update()

    def create_anthill(self, x, y):
        anthill = Anthill(x, y)
        self.drawrect_cords(self, x, y, anthill.color)
        return anthill

    def create_wall(self, x, y):
        self.drawrect_cords(self, x, y, c.WALL_COLOR)
        return x // c.RECT_SIDE * c.RECT_SIDE, y // c.RECT_SIDE * c.RECT_SIDE

    def create_food(self, x, y):
        self.drawrect_cords(self, x, y, c.FOOD_COLOR)
        return x // c.RECT_SIDE * c.RECT_SIDE, y // c.RECT_SIDE * c.RECT_SIDE


class Food:
    def __init__(self, xcor, ycor):
        self.value = c.FOOD_VALUE
        self.xcor = xcor
        self.ycor = ycor

    def draw(self, scr):
        pygame.draw.rect(
            scr,
            c.FOOD_COLOR,
            pygame.rect.Rect((self.xcor, self.ycor),
                             (c.RECT_SIDE, c.RECT_SIDE), width=0),
        )

    def feed(self, ant):
        pass


class Ant(AntGame):
    def __init__(self, scr, xcor, ycor):
        super().__init__(scr)
        self.xcor = xcor
        self.ycor = ycor
        self.color = c.ANT_COLOR
        self.have_food = 0
        self.fer_have_food = c.HAVE_FOOD_FER
        self.dont_have_food = c.DONT_HAVE_FOOD
        self.step_counter = 0
        self.direction = random.randint(0, 90)
        self.last_steps = []
        self.food_distance = []

    def step(self):
        self.step_counter += 1
        if random.random() > 0.95:
            self.direction = random.randint(self.direction - 50, self.direction + 50) % 360

        self.xcor += math.cos(math.radians(self.direction))
        self.ycor += math.sin(math.radians(self.direction))
        if self.xcor > c.SCREEN_WIDTH or self.xcor < 0 or self.ycor > c.SCREEN_HEIGHT or self.ycor < 0:
            self.direction = (self.direction - 90) % 360
        if self.step_counter % 30 == 0:
            self.last_steps.append((self.have_food, (self.xcor, self.ycor), self.step_counter))
        if len(self.last_steps) > 9:
            del self.last_steps[0]

    def draw(self):
        pygame.draw.rect(
            self.scr,
            c.ANT_COLOR,
            pygame.rect.Rect((self.xcor, self.ycor),
                             (3, 3), width=1),
        )

    def draw_fer(self):
        for i in range(0, len(self.last_steps)):
            # print(self.last_steps[:][0])
            if not self.last_steps[i][0]:

                pygame.draw.rect(
                    self.scr,
                    c.DONT_HAVE_FOOD,
                    pygame.rect.Rect((self.last_steps[i][1][0], self.last_steps[i][1][1]),
                                     (1, 1), width=1),
                )
            else:
                pygame.draw.rect(
                    self.scr,
                    c.HAVE_FOOD_FER,
                    pygame.rect.Rect((self.last_steps[i][1][0], self.last_steps[i][1][1]),
                                     (1, 1), width=1),
                )

    def check_wall(self, wall_list: list[tuple[int]]):
        for wall in wall_list:
            if (wall[0] - 1 <= self.xcor <= wall[0] + c.RECT_SIDE + 1) and (
                    wall[1] - 1 <= self.ycor <= wall[1] + c.RECT_SIDE + 1):
                self.direction = (self.direction - 90) % 360

    @staticmethod
    def atan_degree(self, food):
        tan = math.atan((self.ycor - food.ycor) / (self.xcor - food.xcor))
        angel = int(tan * 180 / math.pi) % 360
        if self.xcor > food.xcor:
            angel = (angel - 180) % 360
        return angel

    def anthill_search(self, anthill):
        tan = math.atan((self.ycor - anthill[1]) / (self.xcor - anthill[0]))
        # print(tan)
        angel = int(tan * 180 / math.pi) % 360
        if self.xcor > anthill[0]:
            angel = (angel - 180) % 360
        return angel

    def distance_anthill(self, anthill):
        return math.sqrt((self.xcor - anthill[0]) ** 2 + (self.ycor - anthill[1]) ** 2)

    def find_colors_in_radius(self, scr: pygame.Surface):
        colors_with_coords = []
        # тут происходит проверка радиуса обзора,
        # мы берем и исходный радиус уменьшаем по x и y за счет умножения на sin и cos
        for x in range(-c.RADIUS_ANT, c.RADIUS_ANT):
            for y in range(-c.RADIUS_ANT, c.RADIUS_ANT):
                distance = math.hypot(x, y)
                if distance <= c.RADIUS_ANT:
                    try:
                        pixel_color = scr.get_at((int(x + self.xcor), int(y + self.ycor)))
                        if pixel_color == c.FOOD_COLOR and not self.have_food and {'food': (
                                int(x + self.xcor) // c.RECT_SIDE * c.RECT_SIDE,
                                int(y + self.ycor) // c.RECT_SIDE * c.RECT_SIDE)} not in colors_with_coords:
                            colors_with_coords.append({'food': (int(x + self.xcor) // c.RECT_SIDE * c.RECT_SIDE,
                                                                int(y + self.ycor) // c.RECT_SIDE * c.RECT_SIDE)})
                    except IndexError:
                        # Ignore pixels that are out of bounds
                        pass
                    # pygame.draw.rect(
                    #     self.scr,
                    #     c.ANT_COLOR,
                    #     pygame.rect.Rect((int(x + self.xcor), int(y + self.ycor)),
                    #                      (1, 1), width=1),
                    # )
        return colors_with_coords

    def closer_food(self, all_foods: list[Food]):
        self.food_distance.clear()
        if self.have_food:
            return None
        for food in all_foods:
            self.food_distance.append(int(math.hypot(self.xcor - food.xcor, self.ycor - food.ycor)))
        if min(self.food_distance) < c.RADIUS_ANT:
            closer_food: Food = all_foods[self.food_distance.index(min(self.food_distance))]
            self.direction = self.atan_degree(self, closer_food)
            # print(self.direction)
        if min(self.food_distance) < c.ANT_EAT_LEN:
            self.have_food = True
            food.value -= 1
            self.сolor = c.HAVE_FOOD_FER
