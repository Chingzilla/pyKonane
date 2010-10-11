#src/board_test.py

import unittest
import board

#create shorthand
global b
b = board

class TestBoardFunctions(unittest.TestCase):
    def setUp(self):
        b.SIZE = 6

        self.board_array = [[1, 0, 1, 0, 1, 1],
                            [1, 1, 1, 1, 1, 1], 
                            [1, 1, 0, 1, 1, 1], 
                            [1, 1, 0, 1, 1, 1], 
                            [1, 1, 1, 1, 1, 1], 
                            [1, 1, 1, 1, 1, 1]]

        self.board = b.arrayToBoard(self.board_array)
        
        #print b.toString(self.board)

    def test_isBlack(self):
        #test isBlack
        self.assertTrue(b.isBlack(0,0))
        self.assertTrue(b.isBlack(3,1))
        self.assertTrue(not b.isBlack(0,1))
        self.assertTrue(not b.isBlack(1,0))

        #test isBlackN
        self.assertTrue(b.isBlackN(0))
        self.assertTrue(b.isBlackN(b.SIZE+1))
        self.assertTrue(not b.isBlackN(1))
        self.assertTrue(not b.isBlackN(b.SIZE+4))

    def test_removePeice(self):
        self.assertTrue(b.removePeice(0,0,self.board))
        rp_board = b.removePeice(0,0,self.board)
        self.assertTrue(not b.removePeice(0,0,rp_board))

    def test_validMove(self):
        #fail
        ##out of bounds
        self.assertTrue(not b.isValidMoveN(-1,3,self.board))
        self.assertTrue(not b.isValidMoveN(3, b.SIZE**2 + 1,self.board))
        ##same place
        self.assertTrue(not b.isValidMoveN(5,5,self.board))
        ##(not)same color
        self.assertTrue(not b.isValidMoveN(5,6,self.board))
        ## new place taken
        self.assertTrue(not b.isValidMoveN(0,2,self.board))

        ## old place empty
        self.assertTrue(not b.isValidMoveN(1,3,self.board))

        ## move diaginal
        self.assertTrue(not b.isValidMoveN(8,1,self.board))
        
        ## don't jump over opponete
        self.assertTrue(not b.isValidMoveN(8,20,self.board))

        ##

        
        #success
        # single jump
        self.assertTrue(b.isValidMove([5,0],[3,0],self.board))
        # double jump
        self.assertTrue(b.isValidMove([5,0],[1,0],self.board))
        #fail out-of-bounds

if __name__ == '__main__':
    unittest.main()
