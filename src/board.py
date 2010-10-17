#src/board.py

SIZE = 6

COLOR = {'white': 0,
         'black': 1,
        }

### Board pieces methods ###
def getMask(points):
    '''returns mask created from the n values'''
    if type(points) == int:
        return int(2**points)

    mask = 0
    for x in points:
        mask |= 2**x
    return int(mask)

def getN(col, row):
    return col + row * SIZE

def isBlack(n):
    return not ( n + (n / SIZE) % 2 ) % 2

def getDist(old_n, new_n):
    diff = abs(new_n - old_n)
    if diff < SIZE:
        return diff

    if not diff % SIZE:
        return diff / SIZE
    
    return 0

def getDirection(old_n, new_n):
    '''
    Returns the direction as an Int,
    {1,-1} if left/right
    {SIZE, -SIZE} if up/down
    {0} if on diginal or same place
    '''
    if old_n == new_n:
        return 0
    diff = new_n - old_n
    sign = diff / abs(diff)
    if abs(diff) < SIZE:
        return sign
    
    if not diff % SIZE:
        return sign * SIZE

    return 0

def isPieceAt(n, board):
    mask = getMask(n)
    return bool((mask & board) == mask) 

def getRelitiveN(org_n, rel_col, rel_row):
    '''
    Returns the n value of piece relitive to give piece
    Returns -1 if invalid move
    '''
    org_col, org_row = getXY(org_n)
    
    new_col = org_col + rel_col
    new_row = org_row + rel_row

    if not 0 <= new_col < SIZE:
        return -1
    if not 0 <= new_row < SIZE:
        return -1

    return getN(new_col, new_row)

def getMoveMasks(old_n,new_n):
    rm_m = [old_n]
    mv_m = [new_n]

    dist = getDist(old_n,new_n)
    direct = getDirection(old_n,new_n)

    if dist==direct==0:
        return 0,0

    for i in range(1, dist):
        point = old_n + i * direct
        
        #If odd hop, remove piece
        if not i % 2:
            mv_m.append(point)
        else:
            rm_m.append(point)
    return getMask(rm_m), getMask(mv_m)

def getXY(n):
    '''returns place in form [col,row]'''
    return [n%SIZE, n/SIZE]

def getListOfPieces(board_m):
    '''Returns list of pieces on the board'''
    pieces = []
    for n in range(SIZE**2):
        if board_m & 2**n:
            pieces.append(n)
    return pieces

def getValidMovies(board_m, n):
    '''returns a list about'''
    directions
    pieces = []
    #TODO
    return pieces

def getValidMoviesInDirect(board_m, n, direction):
    '''returns all movies in the given direction'''
    pieces_m = []
    #TODO
    return pieces_m

def getListOfMovies(board_m):
    '''
    returns a list of movies for both red and black pieces
    '''
    board_empty_spaces = board_m ^ getFullBoard()
    empty_spaces = getListOfPieces(board_empty_spaces)
    #TODO
    pass
    

## Checks ##
# all checks return true if passed

def checkOutOfBounds(n):
    return bool(0 <= n < SIZE**2)

def checkIfJump(old_n, new_n):
    '''Checks if the jump is an even number, and that it is a move'''
    dist = getDist(old_n, new_n)
    if dist % 2 == 0 and dist !=0:
        return 1
    return 0

def checkIfPlacesTaken(mask, board):
    board = mask & board
    return mask == board

def checkIfPlacesAvalable(mask, board):
    board = mask & board
    return not bool(board)

## Verify methods ##
# all verify methods return true if passed

def isValidMove(old_n, new_n, board):
    
    # Proper Jump? (also checks if same color and that not same place)
    if not checkIfJump(old_n, new_n):
        return 0

    # In bounds?
    if not checkOutOfBounds(old_n):
        return 0
    if not checkOutOfBounds(new_n):
        return 0

    rm_m, mv_m = getMoveMasks(old_n, new_n)
    # All jump places avaliable?
    if not checkIfPlacesAvalable(mv_m, board):
        return 0

    # Are black peices being jumped?
    if not checkIfPlacesTaken(rm_m, board):
        return 0

    # All checks passed
    return 1

def isValidRemoveBlack(n):
    #Add the corners
    valid_set = [0]
    valid_set.append(getN(SIZE-1,SIZE-1))
    #Add inner square
    valid_set.append(getN((SIZE-1)/2,(SIZE-1)/2))
    valid_set.append(getN(SIZE/2,SIZE/2))
    
    return bool(n in valid_set)

def isValidRemoveWhite(n,black_n):
    if n < 0:
        return 0

    if not isValidRemoveBlack(black_n):
        return 0
    
    white_squares = []
    white_squares.append(getRelitiveN(black_n,-1,0))
    white_squares.append(getRelitiveN(black_n,1,0))
    white_squares.append(getRelitiveN(black_n,0,-1))
    white_squares.append(getRelitiveN(black_n,0,1))

    return bool(n in white_squares)


## Player based method ##
#These methods return modifed boards, 0 if fail

def rmPeice(n, board):
    mask = getMask(n)
    board = board ^ mask
    if board & mask:
        #error, peice wasn't there
        return 0

    return board


### General Board methods ###
def getFullBoard():
    return (2**(6**2) -1)

def toArray(board):
    board_array = []
    for y in range(SIZE):
        board_array.append([])
        for x in range(SIZE):
            if(isPieceAt(getN(x,y),board)):
                board_array[y].append(1)
            else:
                board_array[y].append(0)
    return board_array

def arrayToBoard(board_array):
    '''Takes array in form array[y][x]'''
    #check if board is the right size
    if not len(board_array)==len(board_array[0])==SIZE:
        return 0

    board = 0
    for y in range(len(board_array)):
        for x in range(len(board_array[y])):
            if board_array[y][x]:
                board += 2**getN(x,y)
    
    return board

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
                if isBlack(getN(x,y)):
                    string += 'b'
                else:
                    string += 'w'
            else:
                string += ' '
    return string
