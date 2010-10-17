#!/usr/bin/env python
#src/pyKonane.py

from board import *
import player

COLOR = {'red':0, 'black':1}

def getPlayer(color,p_type=None):
    print "Player Type for {0} pieces".format(color)
    print "0 - Real Player"

    if p_type == None:
        p_type = raw_input('>>> ')

    if p_type == '0':
        return player.Player(color)

    print "Incorrect Option"
    return getPlayer(color)

def main():
    player_1 = getPlayer('black','0')
    player_2 = getPlayer('white','0')

    game_board = getFullBoard()

    print toString(game_board)

    peice = player_1.removePiece(game_board)
    game_board = rmPeice(peice, game_board)

    peice = player_2.removePiece(game_board,peice)
    game_board = rmPeice(peice, game_board)

    print toString(game_board)


if __name__ == '__main__':
    main()
