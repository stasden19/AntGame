import math
import random
import pygame
import constants as c


class Anthill:
    def __init__(self, xcor, ycor):
        self.color = c.COLOR_ANTHILL
        self.xcor = xcor
        self.ycor = ycor

    def draw(self):
        pass


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
        pygame.display.update()

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
                             (10, 10), width=0),
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

    def step(self):
        self.step_counter += 1
        if random.random() > 0.95:
            self.direction = random.randint(self.direction - 50, self.direction + 50) % 360

        self.xcor += math.cos(math.radians(self.direction))
        self.ycor += math.sin(math.radians(self.direction))
        if self.xcor > c.SCREEN_WIDTH or self.xcor < 0 or self.ycor > c.SCREEN_HEIGHT or self.ycor < 0:
            self.direction = (self.direction - 180) % 360
        if self.step_counter % 30 == 0:
            self.last_steps.append((self.have_food, (self.xcor, self.ycor)))
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
            # print(self.last_steps[])
            if self.last_steps[0]:

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
            if (wall[0] - 10 < self.xcor < wall[0] + 10 + c.RECT_SIDE) and (
                    wall[1] - 10 < self.ycor < wall[0] + 10 + c.RECT_SIDE):
                self.direction = (self.direction - 180) % 360

    def find_colors_in_radius(self, scr, radius=c.RADIUS_ANT):
        pygame.draw.circle(scr, (255, 255, 255), (self.xcor, self.ycor), radius, width=1)
        colors_with_coords = []
        for x in range(radius):
            for y in range(radius):
                if x ** 2 + y ** 2 <= 50:
                    # if scr.get_at((int(x+self.xcor), int(y+self.ycor)))[0] == 255:
                    try:
                        pixel_color = scr.get_at((int(x + self.xcor), int(y + self.ycor)))
                    except:
                        continue
                    if pixel_color != (0, 0, 0) and pixel_color != (255, 255, 255, 255) and pixel_color != c.ANT_COLOR and pixel_color != c.WALL_COLOR:
                        colors_with_coords.append((pixel_color, (int(x + self.xcor), int(y + self.ycor))))
        return colors_with_coords
