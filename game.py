import random
import pygame
import constants as c


class Anthill:
    def __init__(self, xcor, ycor):
        self.color = c.COLOR_ANTHILL
        self.xcor = xcor
        self.ycor = ycor

    def spawn(self):
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
    def __init__(self):
        self.value = c.FOOD_VALUE

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
        self.direction = random.randint(0, 7)

    def step(self):
        self.step_counter += 1
        if self.step_counter % 50 == 0:
            self.direction = random.randint(self.direction-1, self.direction+1) % 8
        pygame.draw.rect(
            self.scr,
            c.COLOR_BLACK,
            pygame.rect.Rect((self.xcor, self.ycor),
                             (2, 2), width=1),
        )
        if self.direction == 0:
            self.ycor += 1
        elif self.direction == 1:
            self.ycor += 1
            self.xcor += 1
        elif self.direction == 2:
            self.xcor += 1
        elif self.direction == 3:
            self.xcor += 1
            self.ycor -= 1
        elif self.direction == 4:
            self.ycor -= 1
        elif self.direction == 5:
            self.xcor -= 1
            self.ycor -= 1
        elif self.direction == 6:
            self.xcor -= 1
        elif self.direction == 7:
            self.xcor -= 1
            self.ycor += 1
        if self.xcor > c.SCREEN_WIDTH or self.xcor < 0 or self.ycor > c.SCREEN_HEIGHT or self.ycor < 0:
            self.direction = (self.direction - 2) % 8
        pygame.draw.rect(
            self.scr,
            c.ANT_COLOR,
            pygame.rect.Rect((self.xcor, self.ycor),
                             (2, 2), width=1),
        )

    def check_wall(self, wall_list: list[tuple[int]]):
        for wall in wall_list:
            if pygame.rect.Rect((wall[0] - 5, wall[1] - 5), (c.RECT_SIDE + 10, c.RECT_SIDE + 10)).collidepoint(self.xcor, self.ycor):
                self.direction = (self.direction - 2) % 8
