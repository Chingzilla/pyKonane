#src/board.py

SIZE = 6

COLOR = {'white': 0,
         'black': 1,
        }

#Used to store the know board's weights
known_boards ={}

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

def getValidMoviesInDirect(board_m, n, direction):
    '''
    returns all movies in the given direction
    n is an empty space
    '''
    valid_boards = []
    m = n
    while(1):
        m += direction * 2
        board_move = mvPiece(m, n, board_m)
        if board_move == -1:
            break
        if board_move != -2:
            valid_boards.append(board_move)

    return valid_boards

def getValidMovies(board_m, n):
    '''
    returns a list about
    n is an empty space
    '''
    directions = [-1,1,-SIZE,SIZE]
    valid_boards = []

    for d in directions:
        valid_boards += getValidMoviesInDirect(board_m, n, d)

    return valid_boards

def getListOfMoves(board_m):
    '''
    returns a list of movies for both red and black pieces
    '''
    if known_boards.has_key(board_m):
        return known_boards[board_m]

    board_empty_spaces = board_m ^ getFullBoard()
    empty_spaces = getListOfPieces(board_empty_spaces)
    
    valid_boards_white = []
    valid_boards_black = []
    
    for n in empty_spaces:
        boards = getValidMovies(board_m, n)
        if isBlack(n):
            valid_boards_black += boards
        else:
            valid_boards_white += boards
        
    known_boards[board_m] = [valid_boards_black, valid_boards_white]

    return [valid_boards_black, valid_boards_white]

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

def getBlackRemoves():
    valid_black = []
    #Add corners
    valid_black.append(0)
    valid_black.append(getN(SIZE-1,SIZE-1))
    #Add inner square
    valid_black.append(getN((SIZE-1)/2,(SIZE-1)/2))
    valid_black.append(getN(SIZE/2,SIZE/2))
    
    return valid_black

def getWhiteRemoves(black_n):
    valid_white = []

    valid_directions = [[-1,0], [1,0], [0,-1], [0,1]]
    for v_d in valid_directions:
        next_n = getRelitiveN(black_n, v_d[0], v_d[1])
        if next_n != -1:
            valid_white.append(next_n)
    
    return valid_white

def isValidRemoveBlack(n):
    return bool(n in getBlackRemoves())

def isValidRemoveWhite(n,black_n):
    if n < 0:
        return 0

    if not isValidRemoveBlack(black_n):
        return 0

    return bool(n in getWhiteRemoves(black_n))


## Player based method ##
#These methods return modifed boards, -1 if fail

def rmPiece(n, board):
    if not isPieceAt(n,board):
        return -1

    return board - getMask(n)

def mvPiece(old_n, new_n, board):
    '''
    returns board after move
    returns -1 if error
    returns -2 if starting point is empty
    '''
    direction = getDirection(old_n, new_n)
    if direction == 0: return -1

    #IS piece out of bounds?
    if not (0 <= old_n < SIZE**2):
        return -1
    if not (0 <= new_n < SIZE**2):
        return -1

    #Is there a piece to move?
    if not isPieceAt(old_n, board):
        return -2

    #Pick up piece
    board -= getMask(old_n)
    
    while(old_n != new_n):
        #Is there a piece to jump?
        old_n += direction 
        if not isPieceAt(old_n, board):
            return -1
        #remove piece
        board -= getMask(old_n)

        #Is the next piece open?
        old_n += direction
        if isPieceAt(old_n, board):
            return -1
    
    #Place piece back on the board
    board += getMask(new_n)
    
    return board

### General Board methods ###
def getFullBoard():
    return (2**(SIZE**2) -1)

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
