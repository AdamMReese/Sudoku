from protocol import BOARD_SIZE, UNASSIGNED


def print_board(sudoku_board: list):
    """Function that prints the board"""
    for rows in sudoku_board:
        for cols in rows:
            print(cols, end=' ')
        print()


def empty_pos(sudoku_board: list) -> tuple[int, int] | None:
    """Function that finds an empty position on the board"""
    for i in range(BOARD_SIZE):
        for k in range(BOARD_SIZE):
            if sudoku_board[i][k] == UNASSIGNED:
                return i, k  # (Row, Col)
    return None  # Meaning there is no empty position, so the solver is finished


def check_validation(sudoku_board: list, position: tuple, num: int) -> bool:
    """Functions that checks if the number inputted is valid"""
    row, col = position
    position = (position[0], position[1])

    # Checks the row
    for i in range(BOARD_SIZE):
        if sudoku_board[row][i] == num and (row, i) != position:
            return False

    # Checks the column
    for i in range(BOARD_SIZE):
        if sudoku_board[i][col] == num and (i, col) != position:
            return False

    # Checks the sub-grid
    row = row // 3
    col = col // 3
    for i in range(row * 3, row * 3 + 3):
        for k in range(col * 3, col * 3 + 3):
            if sudoku_board[i][k] == num and (i, k) != position:
                return False
    return True


def solving(sudoku_board: list) -> bool:
    """Functions that handles the backtracking of the solver via recursion"""
    find_empty = empty_pos(sudoku_board)
    if not find_empty:
        return True
    else:
        row, col = find_empty

    for i in range(1, BOARD_SIZE + 1):
        if check_validation(sudoku_board, (row, col), i):
            sudoku_board[row][col] = i
            if solving(sudoku_board):
                return True
            sudoku_board[row][col] = 0
    return False
