from typing import Any
from protocol import BOARD_SIZE
from random import seed, randint
from copy import deepcopy


class DataBase:
    def __init__(self):
        seed(1)
        self.data = None
        self.pre_game = {0: -1, 1: -1, 2: -1, 3: -1}  # 0 - Easy, 1 - Medium, 2 - Hard, 3 - Extreme
        self.easy = []
        self.medium = []
        self.hard = []
        self.extreme = []
        self.get_data_from_file()
        self.process_data(self.data)

    def get_data_from_file(self):
        """Function that gets the data from the file"""
        file_object = open('sudokuData.txt', 'r')
        self.data = file_object.readlines()
        file_object.close()

    def process_data(self, data: list):
        """Function that processes the data from the file and splits it into four strings"""
        for i in range(0, len(data)):
            boards = str(data[i]).split('$')

            if 'EASY' in data[i]:
                boards[len(boards) - 1] = boards[len(boards) - 1][:-1]  # Removes backspace
                self.strings_to_boards(boards[1::], self.easy)

            elif 'MEDIUM' in data[i]:
                boards = boards[:-1]  # Removes backspace
                self.strings_to_boards(boards[1::], self.medium)

            elif 'HARD' in data[i]:
                boards = boards[:-1]  # Removes backspace
                self.strings_to_boards(boards[1::], self.hard)

            elif 'EXTREME' in data[i]:
                self.strings_to_boards(boards[1::], self.extreme)

    def strings_to_boards(self, board: list, level: list):
        """Function that takes the strings and processes them into a game board"""
        temp = [[0] * BOARD_SIZE for i in range(BOARD_SIZE)]

        for string in board:
            if len(string) != (BOARD_SIZE * BOARD_SIZE):
                print("Board size is not correct!")
                continue
            j = 0
            for i in range(0, BOARD_SIZE):
                for k in range(0, BOARD_SIZE):
                    temp[i][k] = int(string[j])
                    j += 1

            level.append(deepcopy(temp))

    def get_rand_board(self, level: int) -> Any | None:
        """Function that sends a random board"""
        if level == 0:
            return self.easy[self.rand_num(self.easy, level)]

        elif level == 1:
            return self.medium[self.rand_num(self.medium, level)]

        elif level == 2:
            return self.hard[self.rand_num(self.hard, level)]

        elif level == 3:
            return self.extreme[self.rand_num(self.extreme, level)]

        print("Wrong level")
        return None

    def rand_num(self, level_lst: list, level_num):
        """Function that randomizes an index to the board, checking to see if the user hasn't played on it before"""
        if len(level_lst) == 1:  # If there is only one board, there's no need to use the while loop
            return 0

        rnd = -1
        while self.pre_game[level_num] == rnd or rnd == -1:
            rnd = randint(0, len(level_lst) - 1)

        self.pre_game[level_num] = rnd
        return rnd
