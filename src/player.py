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
    #@overide
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

def promptForPiece(prompt):
    input = raw_input(str(prompt) + " >>> ")
    input = input.split(',')
    try:
        piece = board.getN(int(input[0]), int(input[1]))
    except:
        print "Envalid Entry, use 'col,row'"
        return promptForPiece(prompt)

    return piece
