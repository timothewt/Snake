from __future__ import annotations
from random import randint
import settings
from settings import np
from Brain import Brain


class Coordinates:
    """
    Coordinates system to simplify the x and y's

    Attribute:
        y:  y position
        x:  x position
    """
    def __init__(self, y: int = 0, x: int = 0) -> None:
        self.y = y
        self.x = x

    def __eq__(self, other: Coordinates) -> bool:
        return self.y == other.y and self.x == other.x

    def __add__(self, other: Coordinates) -> Coordinates:
        return Coordinates(self.y + other.y, self.x + other.x)

    def __str__(self) -> str:
        return f"(y={self.y}, x={self.x})"

    def distance_with(self, other: Coordinates) -> float:
        """
        Computes the distance between two coordinates
        :param other: other coordinates
        :return: the distance between self and other
        """
        return np.sqrt(np.power(self.x - other.x, 2) + np.power(self.y - other.y, 2))


class Snake:
    """
    Core of the game, includes the snake's head, his body, the apple's position

    Attributes:
        origin_head:            coordinates of his head at the instantiation
        origin_apple_position:  coordinates of the apple at the instantiation
        origin_length:          length of the snake at its instantiation
        score:                  current score of the snake which is the number of apples he ate
        high_score:             highest score of the current session
        length:                 length of the snake
        head:                   coordinates of the snake's head
        body:                   coordinates of all the snake's body parts
        orientation:            orientation of the snake's head
        previous_orientation:   orientation of the snake's head before his last move
        movements:              change in coordinates for each orientation
        max_moves:              maximum authorized number of moves
        moves_left:             number of moves left, gets back to the max number each time he eats an apple
        brain:                  brain of the snake that picks his next actions
        ate_apple:              True if he ate an apple during its last move, False otherwise
        died:                   True if he died during its last move, False otherwise
        got_closer_to_apple:    True if he got closer to the apple during its last move, False otherwise
        brain_enabled:          True if the snake picks its orientation by himself
    """
    def __init__(self, head: Coordinates, apple_position: Coordinates, brain_enabled, length: int = 3) -> None:
        self.origin_head = head
        self.origin_apple_position = apple_position
        self.origin_length = length

        self.score = 0
        self.high_score = 0
        self.length = self.origin_length
        self.head = self.origin_head
        self.body = np.array([Coordinates(head.y, head.x - 2), Coordinates(head.y, head.x - 1)])
        self.orientation = 'R'
        self.previous_orientation = 'R'
        self.movements = {'L': Coordinates(0, -1), 'U': Coordinates(-1, 0), 'R': Coordinates(0, 1), 'D': Coordinates(1, 0)}
        self.max_moves = 2 * (settings.X_SIZE + settings.Y_SIZE)
        self.moves_left = self.max_moves

        self.apple_position = self.origin_apple_position

        self.brain = Brain()
        self.ate_apple = False
        self.died = False
        self.got_closer_to_apple = True

        self.brain_enabled = brain_enabled

    def __str__(self) -> str:
        return f'{self.body} {self.head}'

    def update(self) -> None:
        """
        Updates the snake's position and attributes
        """
        self.died = False
        self.ate_apple = False
        self.move()
        if self.brain_enabled:
            self.brain.pick_action(self)

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

    def hits_body(self, new_head: Coordinates) -> bool:
        """
        Detects if the snake will hit its own body if he moves to this location
        :param new_head: new coordinates of the snake's head
        :return: True if he will hit its body, False otherwise
        """
        return new_head in self.body

    def hits_wall(self, new_head: Coordinates) -> bool:
        """
        Detects if the snake will hit a wall if he moves to this location
        :param new_head: new coordinates of the snake's head
        :return: True if he will hit a wall, False otherwise
        """
        return new_head.x < 0 or new_head.x > settings.X_SIZE - 1 or new_head.y < 0 or new_head.y > settings.Y_SIZE - 1

    def move(self) -> None:
        """
        Moves the snake according to its orientation
        """
        new_head = self.head + self.movements[self.orientation]

        if settings.MOVEMENTS[(settings.MOVEMENTS.index(self.previous_orientation) + 2) % 4] == self.orientation:
            # if he tries to go in the opposite direction, behind his head
            self.orientation = self.previous_orientation
            return
        self.previous_orientation = self.orientation
        if self.hits_body(new_head) or self.hits_wall(new_head) or self.moves_left == 1:
            self.got_closer_to_apple = False
            self.on_death()
        elif new_head == self.apple_position:
            self.got_closer_to_apple = True
            self.on_eating_apple(new_head)
        else:
            self.moves_left -= 1
            self.got_closer_to_apple = self.head.distance_with(self.apple_position) > new_head.distance_with(self.apple_position)
            self.shift_body(new_head)

    def on_eating_apple(self, new_head: Coordinates) -> None:
        """
        Called when the snake moves on an apple
        :param new_head: new coordinates of the snake's head
        """
        self.ate_apple = True
        self.body = np.append(self.body, self.head)
        self.head = new_head
        self.length += 1
        self.score += 1
        self.moves_left = self.max_moves
        self.generate_new_apple()

    def game_completed(self) -> bool:
        """
        Checks if the snake takes up all the space of the game, which means there are no remaining space for apples
        :return: True if the game is complete, False otherwise
        """
        return self.length == settings.X_SIZE * settings.X_SIZE

    def generate_new_apple(self) -> None:
        """
        Generates a new apple on the field, that is not placed on the snake
        """
        self.apple_position = Coordinates(randint(0, settings.X_SIZE - 1), randint(0, settings.Y_SIZE - 1))
        while self.apple_position in self.body or self.apple_position == self.head:
            self.apple_position = Coordinates(randint(0, settings.X_SIZE - 1), randint(0, settings.Y_SIZE - 1))

    def on_death(self) -> None:
        """
        When the snake dies, resets its components
        """
        self.died = True

        head = self.origin_head
        self.length = self.origin_length
        self.head = head
        self.body = np.array([Coordinates(head.y, head.x - 2), Coordinates(head.y, head.x - 1)],
                             dtype=Coordinates)
        self.apple_position = self.origin_apple_position
        self.orientation = "R"
        self.previous_orientation = "R"
        self.high_score = max(self.high_score, self.score)
        self.score = 0
        self.moves_left = self.max_moves
