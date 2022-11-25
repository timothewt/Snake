Snake AI - Machine Learning
---
This project aims for an AI that can play Snake using Machine Learning.

<img src="assets/readme.gif" alt="Game Example" width="50%">


Machine Learning used for this project
---
To create this AI I used Tabular Q Learning.<br>
To implement this, we need states and actions. Which means in which state the snake currently is, and which action is
the best in this state.

Here the state consists of 12 booleans:
- 4 for the orientation of the food from the snake's head (on left? up? on right? down?)
- 4 for the surrounding obstacles (an obstacle on its head's left? above? on its right? below?)
- 4 for its orientation (is the snake's facing left? upwards? right? downwards?)

Then for each state, we can either go straight ahead, to the left, or to the right.

The algorithm gives the snake a reward or penalty depending on how beneficial was the action he chose:
- +1 if he got closer to the apple
- -1 if he got further from the apple
- +10 if he ate an apple
- -200 if he died

The formula used at each iteration (after each move) is the Bellman equation:
![](https://wikimedia.org/api/rest_v1/media/math/render/svg/7c8c6f219d5ceabd052cb058a5135bfdac86dc0c)<br>
*Bellman equation (Source: Wikipedia)*

It determines the new value of the action taken in what is called the Q-table, which is just the two-way table with
the states and the action for each state.

Epsilon-greedy (ε) algorithm
---
Another concept used in this project is the epsilon greedy algorithm.

At each action decision, the ε value indicates the probability that the snake picks a completely random action.

This case is called __exploration__ because it explores one of the possibilities that is not labelled as the best. It can lead to learning new moves that could be better.

The other case in which he picks the best moves is __exploitation__.

How to use
---
Install PyGame with `pip install pygame --pre` and then numpy with `pip install numpy`<br>
Then, execute the `main.py` file to run the game.


It can also be played by any user by setting the `play_with_ai` boolean to `False` in the `main.py` file.