# src/player.py

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


def promptForPiece(prompt):
    input = raw_input(str(prompt) + ">>> ")
    input = input.split(',')
    try:
        peice = board.getN(int(input[0]), int(input[1]))
    except:
        print "Envalid Entry, use 'col,row'"
        return promptForPiece(prompt)

    return peice
