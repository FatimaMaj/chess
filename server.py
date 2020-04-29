# Server
from flask import Flask, request, render_template
import json
import time

app = Flask(__name__)

# We use this variable to keep track of when the latest move was made.
# It's only needed to figure out when to send changes to the browser, and save bandwidth when nothing has changed.
latest_move = time.time()

# This variable keeps track of which player's turn it is, so we know which pieces can be moved.
player = 'white'

# This variable keeps track of all the pieces on the board and their positions.
# The first letter is the piece: r(ook), h(orse), b(ishop), k(ing), q(ueen), p(awn)
# The second letter is the color: b(lack), w(hite)
board = [
    ['rb', 'hb', 'bb', 'kb', 'qb', 'bb', 'hb', 'rb'],
    ['pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb', 'pb'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw', 'pw'],
    ['rw', 'hw', 'bw', 'kw', 'qw', 'bw', 'hw', 'rw']
]




# When the user visits the index page, we just show the game's HTML.

@app.route('/')
def http_index():
    return render_template('index.html')


# Every time the user tries to make a move, the client sends an HTTP request to this endpoint. It will contain two URL parameters:
#
# - from: The square from which the user tries to move (A1 notation)
# - to: The square to which the user tries to move (A1 notation)
#
# This method should check whether the move is valid, and then update the board so that the piece has moved and possibly removed another piece at the same time.

def translate_notation(board_square):
    # convert Alphabet column to integer
    # take the first char of board_square e.g ('A1')
    letter = board_square[0]
    board_square_column = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}

    column = board_square_column[letter]
    # take the second char of e.g ('A1')
    number = board_square[1]

    board_square_row = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}

    row = board_square_row[number]

    return row, column

def bishop(from_row, from_column, to_row, to_column, board):
    is_diagonal = abs(to_row - from_row) == abs(to_column - from_column)
    square_in_between = []
    if is_diagonal:
        row = from_row
        column = from_column
        
        # while the bishop is in the way until it reaches to distination
        while row != to_row and column != to_column:
            # bishop moves toward distination 
            # direction is 'top_right'
            if to_row < from_row and to_column > from_column:
                row = row - 1
                column = column + 1
                square_in_between.append(board[row][column])
            
            #direction is 'top_left'
            elif to_row < from_row and to_column < from_column:
                row = row - 1
                column = column - 1
                square_in_between.append(board[row][column])
            
            #direction is 'bottom_left'
            elif to_row > from_row and to_column < from_column:
                row = row + 1
                column = column - 1
                square_in_between.append(board[row][column])
            
            #direction is 'bottom_right'
            elif to_row > from_row and to_column > from_column:
                row = row + 1
                column = column + 1
                square_in_between.append(board[row][column])
       
        # square in between except the last element. We don't need the last element which is the destination
        square_in_between = square_in_between[:-1]
        if all(square is None for square in square_in_between):
            return True
        else:
            return False
    # if not diagonal
    else:
        return False


        
def rook(from_row, from_column, to_row, to_column, board):
    # (horizontal movement): rook can moves in these columns 
    if from_row == to_row:
        # Extract a row from a multi-dimensional array (board)
        rows_of_rook = board[from_row]
        if from_column < to_column:
            #+1, is to not get the square that is player on it
            # square_in_between -> squares in between Origin and Destination of movement
            square_in_between = rows_of_rook[from_column+1 : to_column]
        else:
            square_in_between = rows_of_rook[to_column+1 : from_column]
    
    # (vertical movement): rook can moves in these rows 
    elif from_column == to_column:
        # Extract a column from a multi-dimensional array (board)
        column_of_rook = [row[from_column] for row in board]
        if from_row < to_row:
            square_in_between = column_of_rook[from_row+1 : to_row]
        else:
            square_in_between = column_of_rook[to_row+1 : from_row]
    else:
        return False
    # if all the element in the square_in_between is None. In the other words if there is any piech in the way of rook
    if all(piece is None for piece in square_in_between):
        return True
    else:
        return False


def pawn(from_row, from_column, to_row, to_column, player, board):
    # for white
    move_one_row_up = to_row == from_row - 1
    # for black:
    move_one_row_down = to_row == from_row + 1
    not_move_horizontally = to_column == from_column
    target_is_none = board[to_row][to_column] == None
    same_column = from_column == to_column
    adjacent_column = from_column == to_column - 1 or from_column == to_column + 1
    # len(board) is number of row which is 8
    row_white_before_move = len(board) - 2
    row_black_before_move = 1

    ### rules for white pawn
    if player == 'white':
        # if white pawn is at the first step
        empty_between = board[row_white_before_move - 1][to_column] == None
        if (from_row == row_white_before_move and to_row == row_white_before_move - 2 and
                empty_between and same_column):
            return True

        # if white pawn is in normal walking
        elif move_one_row_up and not_move_horizontally and target_is_none:
            return True

        # Attacking the competitor (white attacking black)
        elif move_one_row_up and adjacent_column and not target_is_none:
            # board[to_row][to_column][1] -> 'pw'; player -> 'white'
            if board[to_row][to_column][1] != player[0]:
                return True
        else:
            return False

    ### rules for black pawn:

    # else if player is black:
    # if black pawn is at the first step, can move two steps
    if player == 'black':
        empty_between = board[row_black_before_move + 1][to_column] == None
        
        if (from_row == row_black_before_move and to_row == row_black_before_move + 2 and
                empty_between and same_column):
            return True

        # if black pawn is in normal walking, can move one step
        if move_one_row_down and not_move_horizontally and target_is_none:
            return True

        # Attacking the competitor (black attacking white)
        elif move_one_row_down and adjacent_column and not target_is_none:
            # board[to_row][to_column][1] -> 'pb', player -> 'black'
            if board[to_row][to_column][1] != player[0]:
                return True
        else:
            return False
    else:
        return False


def horse(from_row, from_column, to_row, to_column, board):
    # All possible moves of a horse
    squares = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    # we can loop over the values directly :
    for square in squares:
        # Position of horse after move
        x = from_column + square[0]
        y = from_row + square[1]
        # if  horse movement is valid
        if x == to_column and y == to_row:
            return True
    return False


def attack_friend(from_row, from_column, to_row, to_column, board):
    destination_position = board[to_row][to_column]
    piece = board[from_row][from_column]

    # If the expression "destination_position is None", we don't run the rest of the expression
    # Second statement after or:  If player want to attack his friend:
    if destination_position is None or piece[1] != destination_position[1]:
        return False
    else:
        return True

@app.route('/move', methods=['POST'])
def http_move():
    global player, board, latest_move

    attack_friend_movement = False
    valid_movement = False

    # These two lines get the "from" and "to" parameters from the URL.
    from_square = request.args['from']
    to_square = request.args['to']

    from_row, from_column = translate_notation(from_square)
    to_row, to_column = translate_notation(to_square)

    # take the piece which want to move
    piece = board[from_row][from_column]

    # If the user tries to make an invalid move, we should return an error message and the HTTP status code 422, which is an error code.
    # return 'Other player should play!', 422

    # (e.g piece = 'pw', 'bw').... player['white'], player['black']
    # If one player, play two times
    if piece[1] != player[0]:
        return 'Other player should play!', 422

    attack_friend_movement = attack_friend(from_row, from_column, to_row, to_column, board)

    if attack_friend_movement:
        return 'You cannot attack your friend', 422


    if piece[0] == 'p':
        valid_movement = pawn(from_row, from_column, to_row, to_column, player, board)
    elif piece[0] == 'h':
        valid_movement = horse(from_row, from_column, to_row, to_column, board)
    elif piece[0] == 'r':
        valid_movement = rook(from_row, from_column, to_row, to_column, board)
    elif piece[0] == 'b':
        valid_movement = bishop(from_row, from_column, to_row, to_column, board)
    
    if valid_movement:
        board[from_row][from_column] = None
        board[to_row][to_column] = piece
        # player: The color of the player whose turn it is now. This should be black if it was white before, and white if it was black before.
        # if movement is valid then next player should play:
        if player == 'white':
            player = 'black'
        elif player == 'black':
            player = 'white'

        # The purpose of "latest_move" variable is described at the top of the file.
        latest_move = time.time()
    else: 
        return 'Invalid Movement', 422

    return {
        'player': player,
        'board': board
    }


# If the user reloads the page (or closes it by mistake and reopens), the client will send a request to this endpoint in order to see the current state of the game and put the pieces where they were before the page was reloaded or closed. This function does not need to be changed.
@app.route('/state')
def http_state():
    if 'since' in request.args:
        latest_poll = float(request.args['since'])
    else:
        latest_poll = None

    if latest_poll is None or latest_move >= latest_poll:
        return {
            'player': player,
            'board': board,
            'changed': latest_move
        }
    else:
        return 'State has not changed', 304