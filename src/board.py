#src/board.py

SIZE = 6



### Board pieces methods ###
def isBlack(col,row):
    return (col + row + 1) % 2

def isBlackN(n):
    return (sum(getXY(n)) + 1) % 2

def getXY(n):
    return [whatCol(n), whatRow(n)]
    
def getTileNum(col,row):
    return col + row * SIZE

def isPieceAt(x,y,board):
    n = getTileNum(x,y)
    return (2**n & board)

def isPieceAtN(n,board):
    return (2**n & board)

def whatRow(n):
    return (n) / SIZE

def whatCol(n):
    return (n) % SIZE


### General Board methods ###
def getFullBoard():
    return (2**(6**2 + 1) - 1)

def toArray(board):
    board_array = []
    for y in range(SIZE):
        board_array.append([])
        for x in range(SIZE):
            board_array[y].append(isPieceAt(x,y,board))
    return board_array

def toString(board):
    '''Serialize board to string'''
    
    board = toArray(board)
    string = '    '
    for i in range(len(board[0])): string += '{0:3d}'.format(i)

    string += '\n    '

    for i in range(len(board)): string += '---'

    for x in range(len(board)):
        string += '\n{0:3d}|'.format(x)
        for y in range(len(board)):
            string += '  '
            if board[x][y]:
                if isBlack(x,y):
                    string += 'b'
                else:
                    string += 'w'
            else:
                string += ' '
    return string
