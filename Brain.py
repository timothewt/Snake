import settings
from settings import np, random
from State import State


class Brain:
    """
    Brain of the snake that picks the next actions

    It uses Machine Learning and more precisely Q Learning.

    For each state of the snake and for each action taken during that state, a value is attributed. The snake picks the
    action with the maximum value and modifies it according to the reward given for this action.

    It also uses and epsilon-greedy algorithm, which means that at random times the program will pick a random direction
    to explore new paths (exploration), otherwise it will pick the best value (exploitation)

    Attributes:
        actions_history:    history of the actions taken for each state
        actions:            possible actions, -1 left, 0 ahead, +1 right
        learning_rate:      learning rate of the algorithm
        discount:           discount factor
        epsilon:            epsilon value for the epsilon-greedy algorithm
        Q_table:            Q-table of the program which contains the values for every action at each possible state
        training_enabled:   If False, does not update the Q-table and disables the epsilon-greedy algorithm
    """

    def __init__(self):
        self.actions_history: list[dict[State | int]] = []
        self.actions: list[int] = [-1, 0, 1]
        self.learning_rate: float = .1
        self.discount: float = .90
        self.epsilon: float = 0.1
        self.Q_table: dict[State:float] = self.read_q_values()

        self.training_enabled: bool = True

    def pick_action(self, snake) -> None:
        """
        Picks an action according to the Q-table, the action which has the greatest value for the current snake's state
        :param snake: snake currently learning
        """
        state = self.get_state(snake)
        try:
            self.Q_table[state]
        except KeyError:  # if the state is not already listed
            self.Q_table[state] = [0, 0, 0]

        if random.uniform(0, 1) < self.epsilon and self.training_enabled:  # only use epsilon when training
            action = self.actions[random.randint(0, 2)]
        else:
            action = self.actions[np.argmax(self.Q_table[state])]

        movement = settings.MOVEMENTS[(settings.MOVEMENTS.index(snake.orientation) + action) % 4]

        if self.training_enabled:
            self.update_Q_table(state, snake)

        self.actions_history.append(
            {
                'state': state,
                'action': action
            }
        )

        snake.orientation = movement

    def update_Q_table(self, state: State, snake) -> None:
        """
        Updates the Q-table according to the Bellman equation:
        Q(s,a) = Q(s,a) + learning_rate * (r + discount * max_a(Q(s',a)) - Q(s,a))
        Where 's' is the previous state, 'a' the action chosen at the state 's', 'r' the reward for the action 'a',
        max_a(Q(s',a)) gives the action which has the greatest value from the state s'
        Here s = prev_state
        :param state: snake's new state (s')
        :param snake: snake currently learning
        """
        if self.actions_history:
            prev_state = self.actions_history[-1]['state']
            q_value = self.Q_table[prev_state][self.actions.index(self.actions_history[-1]['action'])]
            q_value = q_value + self.learning_rate * (
                        self.get_reward(snake) + self.discount * max(self.Q_table[state]) - q_value)
            self.Q_table[prev_state][self.actions.index(self.actions_history[-1]['action'])] = q_value

    def save_q_values(self) -> None:
        """
        Saves the Q-table into the file
        """
        with open('q_values.txt', 'w') as f:
            f.write(str(self.Q_table))

    def read_q_values(self) -> dict[State | list[int]]:
        """
        Read the Q-table from the file
        :return: the Q-table, with the states and valuess
        """
        Q_table = {}
        try:
            with open('q_values.txt', 'r') as f:
                entries = f.read()[1:][:-2].split("], ")
                entries = [entry + "]" for entry in entries]
                for entry in entries:
                    entry = entry.split(": ")
                    values = [float(value) for value in entry[1][1:][:-1].split(', ')]
                    sv = [boolean == 'True' for boolean in entry[0].split("-")]  # state_values
                    state = State(sv[0], sv[1], sv[2], sv[3], sv[4], sv[5], sv[6], sv[7], sv[8], sv[9], sv[10], sv[11])
                    Q_table[state] = values
        except FileNotFoundError:
            pass
        return Q_table

    def get_state(self, snake) -> State:
        """
        Gets the current snake's state, looking for the orientation of the food, the snake and if there are obstacles
        :return: the current State
        """
        return State(
            food_on_left=snake.head.x > snake.apple_position.x,
            food_up=snake.head.y > snake.apple_position.y,
            food_on_right=snake.head.x < snake.apple_position.x,
            food_down=snake.head.y < snake.apple_position.y,
            obstacle_on_left=snake.head.x == 0 or (snake.head + snake.movements["L"]) in snake.body,
            obstacle_up=snake.head.x == 0 or (snake.head + snake.movements["U"]) in snake.body,
            obstacle_on_right=snake.head.x == settings.X_SIZE - 1 or (snake.head + snake.movements["R"]) in snake.body,
            obstacle_down=snake.head.y == settings.Y_SIZE - 1 or (snake.head + snake.movements["D"]) in snake.body,
            orientation_left=snake.orientation == "L",
            orientation_up=snake.orientation == "U",
            orientation_right=snake.orientation == "R",
            orientation_down=snake.orientation == "D"
        )

    def get_reward(self, snake) -> int:
        """
        Determines the reward given from a move made by the snake
        :return: the value of the reward
        """
        if snake.died:
            reward = -200
        elif snake.ate_apple:
            reward = 10
        else:
            if snake.got_closer_to_apple:
                reward = 1
            else:
                reward = -1
        return reward
