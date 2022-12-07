import time
from copy import deepcopy
from random import seed, randint
from typing import Any
import pygame
from buttonClass import Button
from dataBase import DataBase
from protocol import *
from sudokuSolver import solving, check_validation, empty_pos


class App:
    def __init__(self):
        seed(1)
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = None
        self.finished_board = None
        self.temp_values = {}
        self.selected = None
        self.mouse_pos = None
        self.state = "menu"
        self.caption = "Sudoku by Adam Reese"
        self.screen_text = "Sudoku"
        self.start = None
        self.time = None
        self.finished = False
        self.cell_changed = False
        self.error_msg = False
        self.menu_buttons = []
        self.playing_buttons = []
        self.end_game_buttons = []
        self.lock_cells = []
        self.errors = 0
        self.hints = 3
        self.font = pygame.font.SysFont('Arial', 36)
        self.db = DataBase()
        self.load_buttons()

    def run(self):
        while self.running:
            if self.state == 'menu':
                self.menu_events()
                self.menu_update()
                self.menu_draw()

            if self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            if self.state == 'win' or self.state == 'lose':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()

        pygame.quit()

    def menu_events(self):
        """Function that deals with the different events on the menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # What occurs when the user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.menu_buttons:
                    if button.highlighted:
                        button.click()

    def menu_update(self):
        """Function that updates the game (clicking on buttons, etc.)"""
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            button.update(self.mouse_pos)

    def menu_draw(self):
        """Function that draws the menu with the difficulty options"""
        self.window.fill(BLACK)

        for button in self.menu_buttons:
            button.draw(self.window)

        menu_font = pygame.font.SysFont('Arial', 72)
        font = menu_font.render(self.screen_text, False, PINK)
        self.window.blit(font, [195, 35])

        pygame.display.update()
        pygame.display.set_caption(self.caption)

    def get_board(self, level: int):
        """Function that randomly gets a board from the DataBase class and initiate variables from it"""
        self.grid = self.db.get_rand_board(level)
        self.finished_board = deepcopy(self.grid)
        solving(self.finished_board)
        self.load_board()
        self.state = 'playing'
        self.start = time.time()

    def playing_events(self):
        """Function that deals with the events during playing the game"""
        global selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # What occurs when the user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_pos:
                    self.error_msg = False
                    selected = self.mouse_on_grid()

                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.playing_buttons:
                        if button.highlighted:
                            button.click()
                            break

            # When the user types
            if event.type == pygame.KEYDOWN:
                if self.selected is not None and self.selected not in self.lock_cells:  # Checks if the pos is a blank rect
                    if self.is_int(event.unicode):  # Checking if the user entered a number
                        self.temp_values[(self.selected[0], self.selected[1])] = \
                            int(event.unicode)  # temp_values[(x, y)] = num

                    elif event.key == pygame.K_BACKSPACE:
                        del self.temp_values[(self.selected[0], self.selected[1])]

                if event.key == pygame.K_KP_ENTER:
                    pos = (self.selected[0], self.selected[1])
                    if self.finished_board[self.selected[1]][self.selected[0]] == self.temp_values[pos]:  # Checks if the correct number was entered
                        self.grid[self.selected[1]][self.selected[0]] = self.temp_values[pos]  # Adds it to the board
                        del self.temp_values[pos]  # Deletes the value from the temp_values list
                        self.cell_changed = True
                    else:  # Otherwise it is an error
                        self.errors += 1

    def playing_update(self):
        """Function that updates the game when the user clicks on different parts of the board"""
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.playing_buttons:
            button.update(self.mouse_pos)

        if self.cell_changed:
            if empty_pos(self.grid) is None:
                self.state = 'win'
                self.screen_text = 'You Win'
                self.caption = 'Sudoku - Win screen'
                self.game_over_draw()

    def playing_draw(self):
        """Function that draws the game"""
        self.window.fill(WHITE)

        if self.start:
            self.draw_time()

        for button in self.playing_buttons:
            button.draw(self.window)

        if self.selected:  # Checks if the user clicked anywhere on the window
            self.draw_selection(self.window, self.selected)

        if self.grid:
            self.shade_locked_cells(self.window, self.lock_cells)
            self.draw_permanent_numbers(self.window)
            self.draw_user_numbers()
            self.draw_errors(self.window, self.errors)

            if self.error_msg:
                self.draw_error_msg()

            self.draw_grid(self.window)
            pygame.display.update()
            pygame.display.set_caption(self.caption)
            self.cell_changed = False

        if self.errors == 5:
            self.state = 'lose'
            self.screen_text = 'Game Over'
            self.caption = 'Sudoku - Game over'
            self.game_over_draw()

    def game_over_events(self):
        """Function that deals with the different events on the menu (Exiting the game or starting over)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # What occurs when the user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.end_game_buttons:
                    if button.highlighted:
                        button.click()

    def game_over_update(self):
        """Function that updates the menu when the user clicks on it"""
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.end_game_buttons:
            button.update(self.mouse_pos)

    def game_over_draw(self, pos=None):
        """Function that prints the GAME OVER/YOU WIN screen"""
        if pos is None:
            pos = [WIDTH - 460, HEIGHT - 500]
        self.window.fill(BLACK)

        for button in self.end_game_buttons:
            button.draw(self.window)

        error_font = pygame.font.SysFont('Arial', 72)
        font = error_font.render(self.screen_text, False, PINK)
        self.window.blit(font, pos)

        pygame.display.update()
        pygame.display.set_caption(self.caption)

    def draw_permanent_numbers(self, window):
        """Function that draws the numbers on the board"""
        # Draws all the correct numbers on the board
        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != UNASSIGNED:
                    pos = [(x_index * CELL_SIZE) + X_GRID,
                           (y_index * CELL_SIZE) + Y_GRID]  # Getting the number's position
                    self.text_to_screen(self.window, str(num), pos, 1)  # Drawing the numbers

                    # Deletes the values that were guessed from the dict so that only the correct ones are printed
                    if (x_index, y_index) in self.temp_values:
                        del self.temp_values[(x_index, y_index)]

    def draw_user_numbers(self):
        """Function that draws the numbers the user inputs on the board"""
        for x_index, y_index in self.temp_values:
            pos = [(x_index * CELL_SIZE) + X_GRID, (y_index * CELL_SIZE) + Y_GRID]
            self.text_to_screen(self.window, str(self.temp_values[x_index, y_index]), pos, 2)

    def draw_errors(self, window, errors: int):
        """Function that draws the number of errors the user has once they press Enter"""
        x_font = pygame.font.SysFont('Arial', 30)
        font = x_font.render('X', False, RED)
        pos = [0, 0]
        for i in range(0, errors):
            pos[0] = WIDTH - 170 + (i * 20)
            pos[1] = HEIGHT - 560
            window.blit(font, pos)

    def draw_error_msg(self):
        """Function that prints on the screen that the user has used all available hints"""
        pos = [0, 0]
        error_font = pygame.font.SysFont('Arial', 36)
        font = error_font.render('No more hints available', False, RED)
        pos[0] = WIDTH - 490
        pos[1] = HEIGHT - 40
        self.window.blit(font, pos)

    def draw_selection(self, window, selected: list):
        """Function that highlights the selected cell in light blue"""
        pygame.draw.rect(window, PINK,
                         ((selected[0] * CELL_SIZE) + X_GRID, (selected[1] * CELL_SIZE) + Y_GRID, CELL_SIZE, CELL_SIZE))

    def draw_grid(self, window):
        """Function that draws the grid in the window"""
        pygame.draw.rect(window, BLACK, (X_GRID, Y_GRID, WIDTH - X_GRID * 2, HEIGHT - 150), THICKNESS)
        for x in range(1, BOARD_SIZE + 1):
            pygame.draw.line(window, BLACK, (X_GRID + (x * CELL_SIZE), Y_GRID), (X_GRID + (x * CELL_SIZE), 550),
                             THICKNESS if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK, (X_GRID, Y_GRID + (x * CELL_SIZE)),
                             (WIDTH - X_GRID, Y_GRID + (x * CELL_SIZE)), THICKNESS if x % 3 == 0 else 1)

    def draw_time(self):
        """Function that displays the time on the window"""
        self.time = round(time.time() - self.start)
        time_font = pygame.font.SysFont("Arial", 22)
        text = time_font.render("Time: " + self.time_format(), 1, (0, 0, 0))
        self.window.blit(text, (480, 5))

    def time_format(self) -> str:
        """Function that defines the format of the time"""
        sec = self.time % 60
        minute = self.time // 60
        hour = minute // 60
        if hour:
            return str(hour) + ':' + str(minute) + ':' + str(sec)
        return ' ' + str(minute) + ':' + str(sec)

    def mouse_on_grid(self) -> bool | tuple[Any, Any]:
        """Function that checks if the user clicked on the grid or not"""
        # Checks if the user slicked either to the left or above the grid lines
        if self.mouse_pos[0] < X_GRID or self.mouse_pos[1] < Y_GRID:
            return False

        # Checks if the user clicked either to the right or beneath the grid lines
        if self.mouse_pos[0] > (X_GRID + GRID_SIZE) or self.mouse_pos[1] > (Y_GRID + GRID_SIZE):
            return False

        # Returns the position of the mouse on the board
        return (self.mouse_pos[0] - X_GRID) // CELL_SIZE, (self.mouse_pos[1] - Y_GRID) // CELL_SIZE

    def load_board(self):
        """Function that loads the buttons and locked numbers on the screen"""
        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != UNASSIGNED:
                    self.lock_cells.append([x_index, y_index])  # Locking the numbers

    def load_buttons(self):
        """Function that loads the buttons on the board"""
        self.menu_buttons.append(Button(200, 160, 200, 80,
                                        function=self.get_board,
                                        params=0,
                                        colour=WHITE,
                                        text="Easy"))

        self.menu_buttons.append(Button(200, 260, 200, 80,
                                        function=self.get_board,
                                        params=1,
                                        colour=WHITE,
                                        text="Medium"))

        self.menu_buttons.append(Button(200, 360, 200, 80,
                                        function=self.get_board,
                                        params=2,
                                        colour=WHITE,
                                        text="Hard"))

        self.menu_buttons.append(Button(200, 460, 200, 80,
                                        function=self.get_board,
                                        params=3,
                                        colour=WHITE,
                                        text="Extreme"))

        self.playing_buttons.append(Button(90, 40, 100, 40,
                                           function=self.solved_gui,
                                           text="Solve"))

        self.playing_buttons.append(Button(200, 40, 100, 40,
                                           function=self.hint,
                                           text="Hint"))

        self.playing_buttons.append(Button(310, 40, 100, 40,
                                           function=self.try_again,
                                           highlighted_colour=PENCIL_GRAY,
                                           text="Menu"))

        self.end_game_buttons.append(Button(150, 350, 120, 60,
                                            function=self.exit_game,
                                            colour=WHITE,
                                            highlighted_colour=PENCIL_GRAY,
                                            text="Exit"))

        self.end_game_buttons.append(Button(300, 350, 120, 60,
                                            function=self.try_again,
                                            colour=WHITE,
                                            highlighted_colour=PENCIL_GRAY,
                                            text="Try Again"))

    def text_to_screen(self, window, text: str, pos: list, option: int):
        """Function that places the numbers on the screen in a pencil-like format"""
        font = self.font.render(text, False, BLACK if option == 1 else PENCIL_GRAY)
        font_height = font.get_height()
        font_width = font.get_width()
        pos[0] += (CELL_SIZE - font_width) // 2
        pos[1] += (CELL_SIZE - font_height) // 2
        window.blit(font, pos)

    def shade_locked_cells(self, window, lock_cells: list):
        """Function that locks in the number input by the user"""
        for cell in lock_cells:
            pygame.draw.rect(window, GRAY,
                             (cell[0] * CELL_SIZE + X_GRID, cell[1] * CELL_SIZE + Y_GRID, CELL_SIZE, CELL_SIZE))

    def is_int(self, string: str) -> bool:
        """Function that checks if the number input is an integer"""
        try:
            int(string)
            return True
        except:
            return False

    def hint(self):
        """Function that randomly places a correct number on an empty space on the board if the user clicks Hint"""
        if not self.hints:
            self.error_msg = True
            return False
        empty_lst = []
        for i in range(BOARD_SIZE):
            for k in range(BOARD_SIZE):
                if self.grid[i][k] == UNASSIGNED:
                    empty_lst.append((i, k))  # (Row, Col)

        length = len(empty_lst) - 1
        rand_position = randint(0, length)
        self.grid[empty_lst[rand_position][0]][empty_lst[rand_position][1]] = \
            self.finished_board[empty_lst[rand_position][0]][empty_lst[rand_position][1]]
        self.hints -= 1

    def solved_gui(self):
        """Solves the puzzle through backtracking until every number is correct"""
        find = empty_pos(self.grid)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, BOARD_SIZE + 1):
            self.grid[row][col] = i
            self.playing_draw()
            if check_validation(self.grid, [row, col], i):
                if self.solved_gui():
                    return True
            self.grid[row][col] = 0
            pygame.time.delay(150)
        return False

    def try_again(self):
        """Function that redraws the initial values when the game starts over"""
        self.running = True
        self.grid = None
        self.finished_board = None
        self.temp_values = {}
        self.selected = None
        self.mouse_pos = None
        self.state = "menu"
        self.start = None
        self.time = None
        self.caption = "Sudoku"
        self.screen_text = "Sudoku"
        self.start = None
        self.finished = False
        self.cell_changed = False
        self.error_msg = False
        self.lock_cells = []
        self.errors = 0
        self.hints = 3

    def exit_game(self):
        """Function that exits the game"""
        self.running = False


if __name__ == '__main__':
    app = App()
    app.run()
