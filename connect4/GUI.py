import sys
import time

import numpy as np
import pygame
import winsound
from heuristic import *
import minimax
import pruning
import tkinter as tk
from tkinter import simpledialog, messagebox

# size of circle and dimensions of board
SQUARESIZE = 100
ROWS = 6
COLUMNS = 7
K = 1 #max depth
P = 0 #pruning option
RADIUS = SQUARESIZE // 2 - 5
# Colors
COLOR = [(237, 237, 237), (255, 204, 92), (255, 111, 105)] #circle's colors
BOARD_COLOR = (88, 140, 126)

# screen size and dimensions
width = COLUMNS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
size = (width, height)


# set some parameters in a pop up dialog
dialog = tk.Tk()
with_pruning = tk.IntVar()  # 1 if pruning is used, 0 otherwise

def confirm():
    global  K, P
    K = int(k_entry.get())
    P = with_pruning.get()
    print(K, P)
    dialog.destroy()

# pop-up window to take K & play with/without pruning
label = tk.Label(dialog, text="Enter k : ")
label.pack()
k_entry = tk.Entry(dialog)
k_entry.pack()
check_pruning = tk.Checkbutton(dialog, text='With Pruning', variable=with_pruning, onvalue=1, offvalue=0)
check_pruning.pack()
ok_button = tk.Button(dialog, text="Start", command = confirm)
ok_button.pack()
dialog.mainloop()

# initialize BOARD
board = np.zeros((ROWS, COLUMNS), dtype=int)

#displays a circle in the game window
def draw_circle(r, c, color):
    pygame.draw.circle(screen, color, (int((c + 0.5) * SQUARESIZE), int((r + 1.5) * SQUARESIZE)), RADIUS)

#displays a rectangle in the game window
def draw_rect(r, c):
    pygame.draw.rect(screen, BOARD_COLOR, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))

#displays game board
def draw_board(board):
    pygame.draw.rect(screen, COLOR[0], (0, 0, width, SQUARESIZE))
    board = np.flip(board, 0)
    for r in range(ROWS):
        for c in range(COLUMNS):
            draw_rect(r, c)
            draw_circle(r, c, COLOR[board[r][c]])
    pygame.display.update()

#places a piece in the board array for the current turn
def put_piece(board, last_in_row, c, turn):
    row = last_in_row[c]
    if row == ROWS: #move not valid
        return False
    # update the last empty row in column c
    last_in_row[c] += 1
    # put the piece
    board[row][c] = turn
    return True


# update scores
def update_score(board, turn):
    ROWS = len(board)
    COLUMNS = len(board[0])
    score = 0
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == turn and board[r][c] == board[r][c + 1] and board[r][c + 1] == board[r][c + 2] and \
                    board[r][c + 2] == board[r][c + 3]:
                score += 1

    # check COLUMNS
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if board[r][c] == turn and board[r][c] == board[r + 1][c] and board[r + 1][c] == board[r + 2][c] and \
                    board[r + 2][c] == board[r + 3][c]:
                score += 1

    # check +ve diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if board[r][c] == turn and board[r][c] == board[r + 1][c + 1] and board[r + 1][c + 1] == board[r + 2][
                c + 2] and board[r + 2][c + 2] == board[r + 3][c + 3]:
                score += 1

    #check -ve diagonals
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c] == turn and board[r][c] == board[r - 1][c + 1] and board[r - 1][c + 1] == board[r - 2][
                c + 2] and board[r - 2][c + 2] == board[r - 3][c + 3]:
                score += 1

    return score


# initializing empty board
pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

game_over = False
scores = [0, 0] #scores[0] > computer, scores[1] > human
# keep track of last row in each col
last_in_row = np.zeros(COLUMNS, dtype=int)
turn = 0 #computer always goes first
while not game_over:
    if check_end(last_in_row): #check game end
        game_over = True
        print("End")

    elif turn == 0: #computer's turn
        if P == 1:  # with pruning
            start_time = time.time()
            best_move = pruning.decision(board, last_in_row, K)
            total_time = int((time.time() - start_time) * 1000)
            print("time in ms {}".format(total_time))
        else:  # without pruning
            start_time = time.time()
            best_move = minimax.decision(board, last_in_row, K)
            total_time = int((time.time() - start_time) * 1000)
            print("time in ms {}".format(total_time))
        put_piece(board, last_in_row, best_move, turn + 1)
        winsound.PlaySound('mixkit-small-hit-in-a-game-2072.wav', winsound.SND_ASYNC)
        draw_board(board)
        scores[turn] = update_score(board, turn + 1)
        print(scores)
        turn = (turn + 1) % 2
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, COLOR[0], (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = posx // SQUARESIZE
                draw_circle(-1, col, COLOR[turn + 1])
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # human plays
                posx = event.pos[0]
                col = posx // SQUARESIZE
                if not put_piece(board, last_in_row, col, turn + 1):
                   continue


                winsound.PlaySound('mixkit-small-hit-in-a-game-2072.wav', winsound.SND_ASYNC)
                draw_board(board)
                scores[turn] = update_score(board, turn + 1)
                print(scores)
                turn = (turn + 1) % 2
                break
# score pop-up window
messagebox.showinfo("showinfo", "Computer : {} , human : {}".format(scores[0], scores[1]))