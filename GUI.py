from Game import *
import pygame as pg


class GUI:
    def __init__(self):
        self.game = Game()
        self.screen = pg.display.set_mode((15 * 40, 15 * 40 + 40))
        self.directions = {pg.K_UP: "U", pg.K_DOWN: "D", pg.K_LEFT: "L", pg.K_RIGHT: "R"}

    def draw_game(self) -> None:
        """
        Draws all the game's content on the current screen
        """
        self.screen.fill((20, 10, 30))
        self.draw_game_grid()
        self.draw_score_bar()

    def draw_game_grid(self):
        """
        Draws the game's grid which contains the snake and the apple on the current screen
        """
        snake_head = self.game.snake.head
        pg.draw.rect(self.screen, (0, 150, 0), pg.Rect(snake_head.x * 40, snake_head.y * 40, 40, 40))
        apple = self.game.apple_position
        pg.draw.rect(self.screen, (200, 0, 0), pg.Rect(apple.x * 40, apple.y * 40, 40, 40))
        [pg.draw.rect(self.screen, (0, 200, 0), pg.Rect(body_part.x * 40, body_part.y * 40, 40, 40)) for body_part in self.game.snake.body]
        pg.display.update()

    def draw_score_bar(self):
        """
        Draws the score of the game on the bottom of the current screen
        """
        font = pg.font.SysFont('gothambold', 30)
        text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
        pg.draw.rect(self.screen, (50, 30, 60), pg.Rect(0, (self.game.max_y + 1) * 40, (self.game.max_x + 1) * 40, 40))
        self.screen.blit(text, (10, (self.game.max_y + 1) * 40 + 8))
        pg.display.update()

    def draw_controls(self) -> None:
        """
        Draws the controls shown at the start of the game, which are the arrow keys
        """
        x = (self.game.max_x + 1) * 20 - 78  # or * 40 // 2
        y = self.game.max_y * 80 // 3  # or * 40 * 2) // 3
        # left
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(x, y + 53, 50, 50), 1, 4)
        pg.draw.polygon(self.screen, (255, 255, 255), ((x + 40, y + 63), (x + 40, y + 93), (x + 10, y + 78)), 2)
        # down
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(x + 53, y + 53, 50, 50), 1, 4)
        pg.draw.polygon(self.screen, (255, 255, 255), ((x + 63, y + 63), (x + 93, y + 63), (x + 78, y + 93)), 2)
        # right
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(x + 106, y + 53, 50, 50), 1, 4)
        pg.draw.polygon(self.screen, (255, 255, 255), ((x + 146, y + 78), (x + 116, y + 93), (x + 116, y + 63)), 2)
        # up
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(x + 53, y, 50, 50), 1, 4)
        pg.draw.polygon(self.screen, (255, 255, 255), ((x + 63, y + 43), (x + 78, y + 13), (x + 93, y + 43)), 2)
        pg.display.update()

    def draw_game_over(self) -> None:
        """
        Draws a text on the screen depending on the status of the game
        """
        size, string = (35, "Congratulations, you won!") if self.game.snake.game_completed() else (40, "You lost!")
        font = pg.font.SysFont("gothambold", size)
        text = font.render(string, True, (255, 255, 255))
        font_sub = pg.font.SysFont("gothambold", 20)
        text_sub = font_sub.render("Press [R] to restart the game", True, (255, 255, 255))
        x = (self.game.max_x + 1) * 20 - text.get_width() // 2
        y = (self.game.max_y + 1) * 20 - text.get_height() // 2
        self.screen.blit(text, (x, y))
        x_sub = (self.game.max_x + 1) * 20 - text_sub.get_width() // 2
        y_sub = y + size + 15
        self.screen.blit(text_sub, (x_sub, y_sub))
        pg.display.update()

    def on_key_pressed(self, key_pressed: int):
        """
        Picks the new direction of the snake according to the key pressed
        :param key_pressed: number of the pressed key
        """
        try:
            self.game.snake.pick_new_direction(self.directions[key_pressed])
        except KeyError:
            pass

    def restart_game(self) -> None:
        """
        Restarts the game by resetting the game attribute to a new Game object
        """
        self.game = Game()
        self.play()

    def play(self) -> None:
        """
        Main part of the game, manages the key pressed and updates the display each time the snake moves
        """
        pg.init()
        pg.display.set_caption("Snake")
        MOVE = pg.USEREVENT
        pg.time.set_timer(MOVE, 200)  # the snake moves every 200ms
        self.draw_game()
        self.draw_controls()
        has_started = False
        while not has_started:  # loop to make the user press a key before starting the game
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    self.on_key_pressed(event.key)
                    has_started = True
        while True:  # main loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if not self.game.snake.is_alive:
                    if event.type == pg.KEYDOWN and event.key == pg.K_r:
                        self.restart_game()
                    continue
                elif event.type == pg.KEYDOWN:
                    self.on_key_pressed(event.key)
                elif event.type == MOVE:
                    self.game.snake.move()
                    self.draw_game()
                    if not self.game.snake.is_alive:
                        self.draw_game_over()
