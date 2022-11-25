import numpy as np
import pygame as pg
import random


X_SIZE = 40  # grid width
Y_SIZE = 40  # grid height
CELL_SIZE = 20  # px
dt = 25  # ms
SNAKE_X = X_SIZE // 3  # cells
SNAKE_Y = Y_SIZE // 2  # cells
APPLE_X = (3 * X_SIZE) // 4  # cells
APPLE_Y = Y_SIZE // 2  # cells
MOVEMENTS = ["L", "U", "R", "D"]  # movements on the grid
