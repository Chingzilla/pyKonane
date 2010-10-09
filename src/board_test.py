#src/board_test.py

import unittest
import board

#create shorthand
global b
b = board

class TestBoardFunctions(unittest.TestCase):
    def setUp(self):
        b.SIZE = 6

        self.board = [[1, 0, 1, 0, 1, 1],
                      [1, 1, 1, 1, 1, 1], 
                      [1, 1, 0, 1, 1, 1], 
                      [1, 1, 0, 1, 1, 1], 
                      [1, 1, 1, 1, 1, 1], 
                      [1, 1, 1, 1, 1, 1]]

        self.board = board.arrayToBoard(self.board)
    
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

    def test_validmove(self):
        #success
        # single jump
        self.assertTrue(b.isValidMove([0,5],[0,3],self.board))
        # double jump
        self.assertTrue(b.isValidMove([0,5],[0,1],self.board))
        #fail out-of-bounds

if __name__ == '__main__':
    unittest.main()
