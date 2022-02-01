position_weights = [[3, 4, 5, 7, 5, 4, 3],
                    [4, 6, 8, 10, 8, 6, 4],
                    [5, 8, 11, 13, 11, 8, 5],
                    [5, 8, 11, 13, 11, 8, 5],
                    [4, 6, 8, 10, 8, 6, 4],
                    [3, 4, 5, 7, 5, 4, 3]]

ROWS = 6
COLUMNS = 7


# calculate score
def calculate_score(board):
    # initial score
    score = 0

    # check ROW
    ROWS = len(board)
    COLUMNS = len(board[0])
    # weight of 2 ,  3  ,  4
    weights = [50, 1500, 150000]

    # check ROWS
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            count, op, count_empty = check_gps([board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]])
            if count > 1 and count + count_empty == 4:
                score += weights[count - 2]

            elif op > 1 and op + count_empty == 4:
                score -= weights[op - 2]

    # check COLUMNS
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            count, op, count_empty = check_gps([board[r][c], board[r + 1][c], board[r + 2][c], board[r + 3][c]])
            if count > 1 and count + count_empty == 4:
                score += weights[count - 2]

            elif op > 1 and op + count_empty == 4:
                score -= weights[op - 2]

    # check +ve diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            count, op, count_empty = check_gps(
                [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]])
            if count > 1 and count + count_empty == 4:
                score += weights[count - 2]

            elif op > 1 and op + count_empty == 4:
                score -= weights[op - 2]

    # check -ve diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            count, op, count_empty = check_gps(
                [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2], board[r - 3][c + 3]])
            if count > 1 and count + count_empty == 4:
                score += weights[count - 2]

            elif op > 1 and op + count_empty == 4:
                score -= weights[op - 2]

    return score


# counts numbers of yellow, red, and empty places
def check_gps(points):
    count = 0
    op = 0
    count_empty = 0
    for x in points:
        if x == 1:
            count += 1
        elif x == 2:
            op += 1
        elif x == 0:
            count_empty += 1
    return count, op, count_empty


def check_end(last_in_row):
    for c in range(COLUMNS):
        if last_in_row[c] != ROWS:
            return False
    return True


# calculate heuristic
def heuristic(board, last_in_row):
    ROWS = len(board)
    f_sum = 0

    for c, r in enumerate(last_in_row):
        if r != ROWS:
            f_sum += position_weights[r][c]

    return calculate_score(board) * f_sum // 7