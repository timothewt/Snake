from __future__ import annotations


class State:
    """
    Snake's state at a given time.
    Checks for:
        - food's orientation from its head
        - if there are obstacles next to him (on its left, right, above and below him)
        - its orientation (Left, Up, Right, Down)
    """
    def __init__(self, food_on_left: bool, food_up: bool, food_on_right: bool, food_down: bool,
                 obstacle_on_left: bool, obstacle_up: bool, obstacle_on_right: bool, obstacle_down: bool,
                 orientation_left: bool, orientation_up: bool, orientation_right: bool, orientation_down: bool):
        self.food_on_left = food_on_left
        self.food_up = food_up
        self.food_on_right = food_on_right
        self.food_down = food_down

        self.obstacle_on_left = obstacle_on_left
        self.obstacle_up = obstacle_up
        self.obstacle_on_right = obstacle_on_right
        self.obstacle_down = obstacle_down

        self.orientation_left = orientation_left
        self.orientation_up = orientation_up
        self.orientation_right = orientation_right
        self.orientation_down = orientation_down

    def __str__(self):
        return f"{self.food_on_left}-{self.food_up}-{self.food_on_right}-{self.food_down}-{self.obstacle_on_left}-{self.obstacle_up}-{self.obstacle_on_right}-{self.obstacle_down}-{self.orientation_left}-{self.orientation_up}-{self.orientation_right}-{self.orientation_down}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other: State) -> bool:
        return self.food_on_left == other.food_on_left and self.food_up == other.food_up and self.food_on_right == other.food_on_right and self.food_down == other.food_down and self.obstacle_on_left == other.obstacle_on_left and self.obstacle_up == other.obstacle_up and self.obstacle_on_right == other.obstacle_on_right and self.obstacle_down == other.obstacle_down and self.orientation_left == other.orientation_left and self.orientation_up == other.orientation_up and self.orientation_right == other.orientation_right and self.orientation_down == other.orientation_down

    def __hash__(self):
        return hash((self.food_on_left, self.food_up, self.food_on_right, self.food_down, self.obstacle_on_left, self.obstacle_up, self.obstacle_on_right, self.obstacle_down, self.orientation_left, self.orientation_up, self.orientation_right, self.orientation_down))
