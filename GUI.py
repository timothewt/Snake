import settings
from settings import pg
from Snake import Snake, Coordinates


class GUI:
    """
    PyGame GUI for the game.
    Displays the snake and the food on the grid, and below that the score, high score for the session and moves left.

    Attributes:
        snake:      Game's snake
        screen:     current PyGame screen
        directions: direction took by the snake according to the key pressed by the user
    """
    def __init__(self, ai_enabled: bool = True) -> None:
        self.snake = Snake(head=Coordinates(settings.SNAKE_Y, settings.SNAKE_X), apple_position=Coordinates(settings.APPLE_Y, settings.APPLE_X), brain_enabled=ai_enabled)
        self.screen = pg.display.set_mode((settings.X_SIZE * settings.CELL_SIZE, settings.Y_SIZE * settings.CELL_SIZE + 80))
        self.directions = {pg.K_LEFT: "L", pg.K_UP: "U", pg.K_DOWN: "D", pg.K_RIGHT: "R"}

    def draw_game(self) -> None:
        """
        Draws all the game's content on the current screen
        """
        self.draw_game_grid()
        self.draw_score_bar()

    def draw_game_grid(self) -> None:
        """
        Draws the game's grid which contains the snake and the apple on the current screen
        """
        pg.draw.rect(self.screen, (20, 10, 30), pg.Rect(0, 0, settings.X_SIZE * settings.CELL_SIZE, settings.Y_SIZE * settings.CELL_SIZE))
        snake_head = self.snake.head
        pg.draw.rect(self.screen, (0, 150, 0), pg.Rect(snake_head.x * settings.CELL_SIZE, snake_head.y * settings.CELL_SIZE, settings.CELL_SIZE, settings.CELL_SIZE))
        apple = self.snake.apple_position
        pg.draw.rect(self.screen, (200, 0, 0), pg.Rect(apple.x * settings.CELL_SIZE, apple.y * settings.CELL_SIZE, settings.CELL_SIZE, settings.CELL_SIZE))
        [pg.draw.rect(self.screen, (0, 200, 0), pg.Rect(body_part.x * settings.CELL_SIZE, body_part.y * settings.CELL_SIZE, settings.CELL_SIZE, settings.CELL_SIZE)) for body_part in self.snake.body]
        pg.display.update()

    def draw_score_bar(self) -> None:
        """
        Draws the score of the game on the bottom of the current screen
        """
        pg.draw.rect(self.screen, (50, 30, 60), pg.Rect(0, settings.X_SIZE * settings.CELL_SIZE, settings.Y_SIZE * settings.CELL_SIZE, 80))
        font = pg.font.SysFont('gothambold', 30)
        # Score
        score_text = font.render(f"Score: {self.snake.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, settings.Y_SIZE * settings.CELL_SIZE + 8))
        # Score
        high_score_text = font.render(f"High Score: {self.snake.high_score}", True, (255, 255, 255))
        self.screen.blit(high_score_text, (10, settings.Y_SIZE * settings.CELL_SIZE + 48))
        # Moves left
        moves_text = font.render("Moves left: " + str(self.snake.moves_left), True, (255, 255, 255))
        self.screen.blit(moves_text, (settings.X_SIZE * settings.CELL_SIZE - 10 - moves_text.get_width(), settings.Y_SIZE * settings.CELL_SIZE + 8))
        pg.display.update()

    def draw_controls(self) -> None:
        """
        Draws the controls shown at the start of the game, which are the arrow keys
        """
        x = (settings.X_SIZE * settings.CELL_SIZE) // 2 - 78
        y = (settings.Y_SIZE * settings.CELL_SIZE * 2) // 3
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
        size, string = (35, "Congratulations, you won!") if self.snake.game_completed() else (40, "You lost!")
        font = pg.font.SysFont("gothambold", size)
        text = font.render(string, True, (255, 255, 255))
        font_sub = pg.font.SysFont("gothambold", 20)
        text_sub = font_sub.render("Press [R] to restart the game", True, (255, 255, 255))
        x = (settings.X_SIZE + 1) * settings.CELL_SIZE // 2 - text.get_width() // 2
        y = (settings.Y_SIZE + 1) * settings.CELL_SIZE // 2 - text.get_height() // 2
        self.screen.blit(text, (x, y))
        x_sub = (settings.X_SIZE + 1) * settings.CELL_SIZE // 2 - text_sub.get_width() // 2
        y_sub = y + size + 15
        self.screen.blit(text_sub, (x_sub, y_sub))
        pg.display.update()

    def on_key_pressed(self, key_pressed: int) -> bool:
        """
        Picks the new orientation of the snake according to the key pressed
        :param key_pressed: number of the pressed key
        :return True if the key pressed is a correct key for the snake movement, False otherwise
        """
        if key_pressed not in self.directions.keys():
            return False
        self.snake.orientation = self.directions[key_pressed]
        return True

    def restart_game(self) -> None:
        """
        Restarts the game by resetting the game attribute to a new Game object
        """
        self.snake.died = False
        self.play()

    def play(self) -> None:
        """
        Main part of the game, manages the key pressed and updates the display each time the snake moves
        """
        pg.init()
        pg.display.set_caption("Snake - Machine Learning - Q Learning")
        UPDATE = pg.USEREVENT
        pg.time.set_timer(UPDATE, settings.dt)  # the snake moves every 200ms
        self.draw_game()
        self.draw_controls()
        has_started = False
        while not has_started:  # loop to make the user press a key before starting the game
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    has_started = self.on_key_pressed(event.key)
        while True:  # main loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.snake.brain.save_q_values()
                    exit()
                if not self.snake.brain_enabled and self.snake.died:  # only displays if a real user is playing
                    if event.type == pg.KEYDOWN and event.key == pg.K_r:
                        self.restart_game()
                    continue
                elif event.type == pg.KEYDOWN:
                    self.on_key_pressed(event.key)
                elif event.type == UPDATE:
                    self.snake.update()
                    self.draw_game()

                    if not self.snake.brain_enabled and self.snake.died:  # only displays game over if a real user is playing
                        self.draw_game_over()
