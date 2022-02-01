import sys
from heuristic import *
from pptree import *
from queue import PriorityQueue

# entry point
'''
board : numpy array > game board
last_in_row : array > stores the last available row in each column in the board
k : integer         > maximum depth in the decision tree
'''


def decision(board, last_in_row, k):
    root = Node(" max")  # for printing the decision tree
    best_move, best_score, node_count = maximizer(board, last_in_row, 0, k, -sys.maxsize - 1, sys.maxsize, root)
    root.name += " :: {} nodes expanded".format(node_count + 1)
    #print_tree(root)  # print decision tree
    print(f"{node_count + 1} nodes expanded")
    return best_move  # return decided column


'''
depth : int > depth of the current tree node
alpha : int > lower bound on max 
beta  : int > upper bound on min
root : Node > parent node
'''


def maximizer(board, last_in_row, depth, k, alpha, beta, root):
    if check_end(last_in_row):  # terminal state. board is complete, 1000 x final score is returned
        val = 1000 * calculate_score(board)
        root.name += ",score: " + str(val) + " "
        return -1, val, 0

    if depth == k:  # depth limit reached, evaluate using the heuristic
        val = heuristic(board, last_in_row)
        root.name += ",score: " + str(val) + " "
        return -1, val, 0

    max_child, max_score = -1, -sys.maxsize - 1
    ROWS = len(board)
    q = PriorityQueue()
    # insert nodes in a priority queue with key equal to position weight
    # this reorders nodes to maximize pruning. decisions with highest position weights are more likely to be good decisions
    for c, r in enumerate(last_in_row):
        if r != ROWS:
            q.put((position_weights[r][c], r, c))

    node_count = 0
    # examin valid decisions
    while not q.empty():
        w, r, c = q.get()
        board[r][c] = 1
        last_in_row[c] += 1
        curr_root = Node(" min", root)  # for printing decision tree
        # next is minimizer's turn
        child, child_score, next_count = minimizer(board, last_in_row, depth + 1, k, alpha, beta, curr_root)
        board[r][c] = 0
        last_in_row[c] -= 1
        node_count += 1 + next_count
        if child_score > max_score:
            max_child, max_score = c, child_score
            s = ",score: " + str(max_score) + ",nxt: " + str(max_child) + " "  # for printing the decision tree

        if max_score >= beta:
            break
        if max_score > alpha:
            alpha = max_score

    root.name += s  # for printing the decision tree
    return max_child, max_score, node_count


def minimizer(board, last_in_row, depth, k, alpha, beta, root):
    if check_end(last_in_row):  # terminal state. board is complete, 1000 x final score is returned
        val = 1000 * calculate_score(board)
        root.name += ",score: " + str(val) + " "
        return -1, val, 0

    if depth == k:  # depth limit reached, evaluate using the heuristic
        val = heuristic(board, last_in_row)
        root.name += ",score: " + str(val) + " "
        return -1, val, 0

    min_child, min_score = -1, sys.maxsize
    ROWS = len(board)
    q = PriorityQueue()
    # insert nodes in a priority queue with key equal to position weight
    # this reorders nodes to maximize pruning. decisions with highest position weights are more likely to be good decisions
    for c, r in enumerate(last_in_row):
        if r != ROWS:
            q.put((-1 * position_weights[r][c], r, c))

    node_count = 0
    # examin valid decisions
    while not q.empty():
        w, r, c = q.get()
        board[r][c] = 2
        last_in_row[c] += 1
        curr_root = Node(" max", root)  # for printing decision tree
        # next is maximizer's turn
        child, child_score, next_count = maximizer(board, last_in_row, depth + 1, k, alpha, beta, curr_root)
        board[r][c] = 0
        last_in_row[c] -= 1
        node_count += 1 + next_count
        if child_score < min_score:
            min_child, min_score = c, child_score
            s = ",score: " + str(min_score) + ",nxt: " + str(min_child) + " "  # for printing the decision tree
        if min_score <= alpha:
            break
        if min_score < beta:
            beta = min_score

    root.name += s  # for printing the decision tree
    return min_child, min_score, node_count