# Server
from flask import Flask, request, render_template

app = Flask(__name__)

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


def rook(from_row, from_column, to_row, to_column, board):
    if from_row == to_row or from_column == to_column:
        return True
    else:
        False


def pawn(from_row, from_column, to_row, to_column, player, board):
    # for white
    move_one_row_up = to_row == from_row - 1
    # for black:
    move_one_row_down = to_row == from_row + 1
    not_move_horizontally = to_column == from_column
    target_is_none = board[to_row][to_column] == None
    adjacent_column = from_column == to_column - 1 or from_column == to_column + 1
    row_white_before_move = len(board) - 2
    row_black_before_move = 1

    ### rules for white pawn
    if player == 'white':
        # if white pawn is at the first step
        # len(board) is number of row which is 8
        if from_row == row_white_before_move and to_row == row_white_before_move - 2 and \
                board[row_white_before_move - 1][to_column] == None:
            return True

        # if white pawn is in normal walking
        elif move_one_row_up and not_move_horizontally and target_is_none:
            return True

        # Attacking the competitor (white attacking black)
        elif move_one_row_up and adjacent_column and not target_is_none:
            # board[to_row][to_column][1] -> 'pw'; player -> 'white'
            if (board[to_row][to_column][1] != player[0]):
                return True
        else:
            return False

    ### rules for black pawn:

    # else if player is black:
    # if black pawn is at the first step, can move two steps
    if player == 'black':
        # len(board) -
        if from_row == row_black_before_move and to_row == row_black_before_move + 2 and \
                board[row_black_before_move + 1][to_column] == None:
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
    global player, board

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
    
    if valid_movement:
        board[from_row][from_column] = None
        board[to_row][to_column] = piece
        # player: The color of the player whose turn it is now. This should be black if it was white before, and white if it was black before.
        # if movement is valid then next player should play:
        if player == 'white':
            player = 'black'
        elif player == 'black':
            player = 'white'

    return {
        'player': player,
        'board': board
    }


# If the user reloads the page (or closes it by mistake and reopens), the client will send a request to this endpoint in order to see the current state of the game and put the pieces where they were before the page was reloaded or closed. This function does not need to be changed.


@app.route('/state')
def http_state():
    return {
        'player': player,
        'board': board
    }
