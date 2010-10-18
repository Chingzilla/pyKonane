# src/player.py

import random

import board
from board import COLOR

class Player(object):
    '''
    Default player class
    '''
    def __init__(self, color):
        self.color = color

    def removePiece(self, g_board, black_n=None):
        print "{0} player's turn ----".format(self.color)
        print board.toString(g_board)
        while(1):
            input = promptForPiece("Remove {0} piece".format(self.color))
            if COLOR[self.color] == COLOR['black']:
                if board.isValidRemoveBlack(input):
                    return input
            else:
                if board.isValidRemoveWhite(input,black_n):
                    return input
            print "Invalid Piece Removed: {0}".format(input)

    def movePiece(self, g_board):
        print "{0} player's turn ----".format(self.color)
        print board.toString(g_board)
        while(1):
            old_piece = promptForPiece("Old piece to move")
            new_piece = promptForPiece("New place to move")
            new_board = board.mvPiece(old_piece, new_piece, g_board)
            if new_board != -1 and COLOR[self.color] == board.isBlack(old_piece):
                return new_board
            print "Invalid Move"

class Player_Random(Player):
    '''
    Player that plays randomly
    '''
    def removePiece(self, g_board, black_n=None):
        if self.color == 'black':
            choice = random.choice(board.getBlackRemoves())
        else:
            choice = random.choice(board.getWhiteRemoves(black_n))
        
        print "{0} player removes {1}".format(self.color, choice)
        return choice
    
    def movePiece(self, g_board):
        print "Random {0} player's turn ----".format(self.color)
        print board.toString(g_board)

        choices = board.getListOfMoves(g_board)
        if self.color == 'black':
            choices = choices[0]
        else:
            choices = choices[1]
        
        return random.choice(choices)

class Player_MinMax(Player_Random):
    '''
    Player that plays with MinMax
    Black = Max player = 0
    White = Min player = 1
    '''
    def __init__(self, color, depth=None):
        self.color = color
        if depth == None:
            depth = int(raw_input("Max depth >>>"))
        self.depth = depth

class Player_AlphaBeta(Player_MinMax):
    '''
    Same as Player_MinMax, but with extra pruning logic
    '''

def minmax_Decision(state):
    state = board.getListOfMoves(state)

    num_moves_black = len(state[0])
    num_moves_white = len(state[1])
    
    value = num_moves_black - num_moves_white
    
    # weight results if at terminal
    if num_moves_white == 0:
        value += 50
        state[3] = value

    if num_moves_black == 0:
        value -= 50
        state[4] = value

    return value

def minmax_Max(board, depth):
    actions = getListOfMoves(board)[0]
    # See if at terminal node or max depth
    if depth >= MAX_DEPTH or getListOfMoves(board)[1] == 0:
        return minmax_Decision(board)
    
    v = -float('int')
    depth += 1
    for a in acitons:
        v_temp = minmax_Min(a,int(not player), depth)
        if v_temp > v:
            v = v_temp
    return v

def minmax_Min(board, depth):
    actions = getListOfMoves(board)[1]
    # See if at terminal node or max depth
    if depth >= MAX_DEPTH or getListOfMoves(board)[0] == 0:
        return minmax_Decision(board)
    
    v = -float('int')
    depth += 1
    for a in acitons:
        v_temp = minmax_Max(a,int(not player), depth)
        if v_temp < v:
            v = v_temp
    return v

def getHeuristicBlack(current_board):
    board.getListOfMoves(current_board)
    
    current_board = board.known_boards[current_board]

    num_of_black_moves, num_of_white_moves = board.getListOfMoves(board)[0:1]
    num_of_black_moves = len(num_of_black_moves)
    mun_of_white_moves = len(num_of_white_moves)
    
    # Weight results
    if num_of_black_moves == 0 and turns_color == "white":
        num_of_white_moves += 100
    elif num_of_white_moves == 0 and turn_color == "black":
        num_of_black_moves += 100

    heuristic = num_of_black_moves - num_of_white_moves

    return

def promptForPiece(prompt):
    input = raw_input(str(prompt) + " >>> ")
    input = input.split(',')
    try:
        piece = board.getN(int(input[0]), int(input[1]))
    except:
        print "Envalid Entry, use 'col,row'"
        return promptForPiece(prompt)

    return piece
