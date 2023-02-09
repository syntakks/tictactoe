"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
 

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xCount = 0
    oCount = 0
    
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == X:
                xCount += 1
            if board[i][j] == O:
                oCount += 1
    
    if xCount == 0 and oCount == 0:
        return X

    if xCount > oCount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    remainingActions = []

    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if not board[i][j]:
                remainingActions.append((i, j))

    return remainingActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    actingPlayer = player(board)
    board[action[0]][action[1]] = actingPlayer

    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Board
    # 0, 1, 2
    # 3, 4, 5
    # 6, 7, 8 

    # Flatten Board
    flatBoard = [col if col else "-" for rows in board for col in rows]

    # Check for Initial State
    if all(pos == "-" for pos in flatBoard):
        return None
    
    triplets = []

    # Rows
    triplets.append("".join(flatBoard[:3]))
    triplets.append("".join(flatBoard[3:6]))
    triplets.append("".join(flatBoard[6:9]))

    # Columns
    triplets.append("".join(flatBoard[0] + flatBoard[3] + flatBoard[6]))
    triplets.append("".join(flatBoard[1] + flatBoard[4] + flatBoard[7]))
    triplets.append("".join(flatBoard[2] + flatBoard[5] + flatBoard[8]))

    # Diagonal
    triplets.append("".join(flatBoard[0] + flatBoard[4] + flatBoard[8]))
    triplets.append("".join(flatBoard[2] + flatBoard[4] + flatBoard[6])) 

    for triplet in triplets:
        winner = triplet_winner(triplet)
        if winner:
            return winner

    return None
    
def triplet_winner(triplet):
    """
    Returns winner for a row/ col/ diagonal if it has one, otherwise None.
    """
    if any(letter == '-' for letter in triplet):
        return None
    if all(letter == X for letter in triplet):
        return X
    if all(letter == O for letter in triplet):
        return O

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    hasWinner = winner(board) is not None
    noActionsAvailable = len(actions(board)) == 0
    return hasWinner or noActionsAvailable

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    champion = winner(board)
    if champion == X:
        return 1
    if champion == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    minimax_board = copy.deepcopy(board)

    minimax_actions = actions(minimax_board)

    minimax_player = player(minimax_board)

    best_score = -math.inf if is_maximizing(minimax_player) else math.inf
    best_action = None
    best_depth = 0

    for action in minimax_actions:
        nextBoard = result(minimax_board, action)
        nextPlayer = player(nextBoard)
        
        if is_maximizing(nextPlayer):
            (value, depth) = max_value(nextBoard, best_depth)
            print("--------")
            print(f'max: action: {action}, value: {value}, depth: {depth}')
            if value > best_score:
                best_score = value
                best_action = action
                best_depth = depth 
        else:
            (value, depth) = min_value(nextBoard, best_depth)
            print("--------")
            print(f'min: action: {action}, value: {value}, depth: {depth}')
            if value < best_score:
                best_score = value
                best_action = action
                best_depth = depth 
    
    print('************************')
    print(f'best score: {best_score}')
    print(f'best action: {best_action}')
    print(f'depth: {best_depth}')
    print('***********************')
    return best_action

def max_value(board, depth):
    # Check Terminal
    if terminal(board):
        return (utility(board), depth)

    value = -math.inf

    for action in actions(board):
        print(f'max: depth: {depth}')
        nextValue, nextDepth = min_value(result(board, action), depth + 1)
        value = max(value, nextValue)
    
    return (value, nextDepth)
    

def min_value(board, depth):
    # Check Terminal
    if terminal(board):
        return (utility(board), depth)

    value = math.inf

    for action in actions(board):
        print(f'min: depth: {depth}')
        nextValue, nextDepth = max_value(result(board, action), depth + 1)
        value = min(value, nextValue)
    
    return (value, nextDepth)
        

def is_maximizing(player):
    return player == X