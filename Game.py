from random import randint
from Snake import *


class Game:
    def __init__(self):
        self.score = 0
        self.max_y = 14
        self.max_x = 14
        self.apple_position = Coordinates(y=7, x=10)
        self.snake = Snake(game=self, head_y=7, head_x=4, length=3)

    def __str__(self) -> None:
        game = ""
        for i in range(0, self.max_y):
            for j in range(0, self.max_x):
                current = Coordinates(i, j)
                if self.apple_position == current:
                    game += "a"
                elif current in self.snake.body:
                    game += "b"
                elif current == self.snake.head:
                    game += "s"
                else:
                    game += "_"
                game += " "
            game += "\n"
        return game

    def generate_new_apple(self) -> None:
        """
        Generates a new apple on the field, that is not placed on the snake
        """
        self.apple_position = Coordinates(randint(0, self.max_y), randint(0, self.max_x))
        while self.apple_position in self.snake.body or self.apple_position == self.snake.head:
            self.apple_position = Coordinates(randint(0, self.max_y), randint(0, self.max_x))

