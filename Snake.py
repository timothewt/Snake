from __future__ import annotations

from random import randint

import numpy as np
import settings


class Coordinates:
    def __init__(self, y: int = 0, x: int = 0) -> None:
        self.y = y
        self.x = x

    def __eq__(self, other: Coordinates) -> bool:
        return self.y == other.y and self.x == other.x

    def __add__(self, other: Coordinates) -> Coordinates:
        return Coordinates(self.y + other.y, self.x + other.x)


class Snake:
    def __init__(self, head_y: int, head_x: int, apple_position: Coordinates, length: int = 3) -> None:
        self.score = 0
        self.length = length
        self.head = Coordinates(head_y, head_x)
        self.body = np.array([Coordinates(head_y, head_x - 2), Coordinates(head_y, head_x - 1)], dtype=Coordinates)
        self.direction = 'R'
        self.movements = {'R': Coordinates(0, 1), 'L': Coordinates(0, -1), 'U': Coordinates(-1, 0), 'D': Coordinates(1, 0)}
        self.is_alive = True
        self.apple_position = apple_position

    def __str__(self) -> str:
        return f'{self.body} {self.head}'

    def shift_body(self, new_head: Coordinates) -> None:
        """
        Shifts the body from its previous location to the new, by shifting the list of the body and replacing its last
        element with the new head coordinates.
        :param new_head: new coordinates of the snake's head
        """
        for i in range(0, self.length - 2):
            self.body[i] = self.body[i + 1]
        self.body[-1] = self.head
        self.head = new_head

    def will_hit_body(self, new_head: Coordinates) -> bool:
        """
        Detects if the snake will hit its own body if he moves to this location
        :param new_head: new coordinates of the snake's head
        :return: True if he will hit its body, False otherwise
        """
        return new_head in self.body

    def will_hit_wall(self, new_head: Coordinates) -> bool:
        """
        Detects if the snake will hit a wall if he moves to this location
        :param new_head: new coordinates of the snake's head
        :return: True if he will hit a wall, False otherwise
        """
        return new_head.x < 0 or new_head.x > settings.X_SIZE or new_head.y < 0 or new_head.y > settings.Y_SIZE

    def move(self) -> bool:
        """
        Moves the snake according to its direction
        :return: True if the snake survived to the move, False otherwise
        """
        new_head = self.head + self.movements[self.direction]
        if self.is_going_back(self.direction):
            return True
        if self.will_hit_body(new_head) or self.will_hit_wall(new_head):
            self.is_alive = False
            return False
        if new_head == self.apple_position:
            self.on_eating_apple(new_head)
        else:
            self.shift_body(new_head)
        return True

    def is_going_back(self, direction: str) -> bool:
        """
        Checks if the snake is going onto his own body by going backwards, e.g. his head goes on his first piece of body
        :param direction: direction of the movement: R,L,U,D
        :return: True if he is going back onto himself, False otherwise
        """
        new_head = self.head + self.movements[direction]
        return new_head == self.body[-1]

    def on_eating_apple(self, new_head: Coordinates) -> None:
        """
        Called when the snake moves on an apple
        :param new_head: new coordinates of the snake's head
        """
        self.body = np.append(self.body, self.head)
        self.head = new_head
        self.length += 1
        self.score += 1
        self.generate_new_apple()

    def game_completed(self) -> bool:
        """
        Checks if the snake takes up all the space of the game, which means there are no remaining space for apples
        :return: True if the game is complete, False otherwise
        """
        return self.length == settings.X_SIZE * settings.X_SIZE

    def pick_new_direction(self, direction: str) -> None:
        """
        Picks a new direction if the snake is not going back
        :param direction: new direction: R,L,U,D
        """
        if not self.is_going_back(direction):
            self.direction = direction

    def generate_new_apple(self) -> None:
        """
        Generates a new apple on the field, that is not placed on the snake
        """
        self.apple_position = Coordinates(randint(0, settings.X_SIZE - 1), randint(0,  settings.Y_SIZE - 1))
        while self.apple_position in self.body or self.apple_position == self.head:
            self.apple_position = Coordinates(randint(0, settings.X_SIZE - 1), randint(0, settings.Y_SIZE - 1))
