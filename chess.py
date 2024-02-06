

"""checking if the figures can move like the player wants them to and if nothing is in way"""
def white_pawn_legal(begin, end, color, board):

    row_0 = begin[0]
    col_0 = begin[1]

    row_1 = end[0]
    col_1 = end[1]

    if (col_0 == col_1 and row_1+1 == row_0) and board[row_1][col_1] == ".":    #going up by 1
        return True

    if row_0 == 6:
        if (col_0 == col_1 and row_1 + 2  == row_0) and board[row_1][col_1] == ".":  #going up by 2 from base position
            return True

    if  (row_1 + 1 == row_0) and abs(col_1 - col_0) == 1 and board[row_1][col_1].islower():   #taking diagonally
        return True

    return False


def black_pawn_legal(begin, end, color, board):

    row_0 = begin[0]
    col_0 = begin[1]

    row_1 = end[0]
    col_1 = end[1]

    if (col_0 == col_1 and row_1-1 == row_0) and board[row_1][col_1] == ".":    #going down by 1
        return True

    if row_0 == 1:
        if (col_0 == col_1 and row_1 - 2  == row_0) and board[row_1][col_1] == ".":  #going up by 2 from base position
            return True


    if  (row_1 - 1 == row_0) and abs(col_1 - col_0) == 1 and board[row_1][col_1].isupper():   #taking diagonally
        return True

    return False


def knight_legal(begin, end, color, board):

    row_0 = begin[0]
    col_0 = begin[1]

    row_1 = end[0]
    col_1 = end[1]

    if board[row_1][col_1].isupper() and color == "white":
        return False

    if board[row_1][col_1].islower() and color == "black":
        return False

    if abs(row_1-row_0) == 2 and abs(col_1 - col_0) == 1:   #two rows up/down, one column right/left
        return True

    if abs(row_1-row_0) == 1 and abs(col_1 - col_0) == 2:
        return True


    return False


def rook_legal(begin, end, color, board):

    row_0 = begin[0]
    col_0 = begin[1]

    row_1 = end[0]
    col_1 = end[1]

    if row_0 != row_1 and col_0 != col_1:       #not moving like rook
        return False


    """checking if anything stands in way of movement except for last """
    """first in same row"""
    if row_0 == row_1:
        for i in range(min(col_0, col_1) + 1, max(col_0, col_1)):
            if board[row_0][i] != ".":
                return False
    #then in same column
    else:
        for i in range(min(row_0, row_1) + 1, max(row_0, row_1)):
            if board[i][col_0] != ".":
                return False

    if color == "white" and board[row_1][col_1].isupper():
        return False

    if color == "black" and board[row_1][col_1].islower():
        return False

    return True


def bishop_legal(begin, end, color, board):
    row_0 = begin[0]
    col_0 = begin[1]

    row_1 = end[0]
    col_1 = end[1]


    if abs(row_1-row_0) != abs(col_1-col_0):
        return False


    step_row = -1 if row_0 > row_1 else 1
    step_col = -1 if col_0 > col_1 else 1
    if row_0 == row_1 and col_0 == col_1:
        step_row = 0
        step_col = 0

    r, c = row_0 + step_row, col_0 + step_col

    """checking all but last position in the way"""

    while r != row_1 and c != col_1:
        if board[r][c] != ".":
            print("na ah")
            return False
        r += step_row
        c += step_col
    if (color == "white" and board[row_1][col_1].isupper()) or (color == "black" and board[row_1][col_1].islower()):
        return False

    return True

def queen_legal(begin, end, color, board):
    return rook_legal(begin, end, color, board) or bishop_legal(begin, end, color, board)

def king_legal(begin, end, color, board):

    row_0 = begin[0]
    col_0 = begin[1]

    row_1 = end[0]
    col_1 = end[1]

    if board[row_1][col_1].isupper() and color == "white":
        return False

    if board[row_1][col_1].islower() and color == "black":
        return False

    if max(abs(row_1 - row_0), abs(col_1 - col_0)) > 1:
        return False

    return True

def legal_move(chosen_figure, begin, end, color, board):


    if chosen_figure == "P" and white_pawn_legal(begin, end, color, board):
        return True

    if chosen_figure == "p" and black_pawn_legal(begin, end, color, board):
        return True

    if (chosen_figure == "R" and rook_legal(begin, end, "white", board)) or (chosen_figure == "r" and rook_legal(begin, end, "black", board)) :
        return True

    if (chosen_figure == "N" and knight_legal(begin, end, "white", board)) or (chosen_figure == "n" and knight_legal(begin, end, "black", board)):
        return True

    if (chosen_figure == "B" and bishop_legal(begin, end, "white", board)) or (chosen_figure == "b" and bishop_legal(begin, end, "black", board)):
        return True

    if (chosen_figure == "Q" and queen_legal(begin, end, "white", board)) or (chosen_figure == "q" and queen_legal(begin, end, "black", board)):
        return True

    if (chosen_figure == "K" and king_legal(begin, end, "white", board)) or (chosen_figure == "k" and king_legal(begin, end, "black", board)):
        return True

    return False



def white_king_checked(board):
    # Find the position of the white king
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == "K":
                king_pos = row, col
                break
        if king_pos:
            break

    end = row, col

    # Check if any black piece can attack the white king
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            begin = row, col

            if piece.islower():  # It's a black piece
                #print(piece, begin)

                if (piece == "p" and black_pawn_legal(begin, end, "black", board)) or \
                   (piece == "n" and knight_legal(begin, end, "black", board)) or \
                   (piece == "r" and rook_legal(begin, end, "black", board)) or \
                   (piece == "b" and bishop_legal(begin, end, "black", board)) or \
                   (piece == "q" and queen_legal(begin, end, "black", board)) or \
                   (piece == "k" and king_legal(begin, end, "black", board)):
                    print(piece)
                    return True

    return False



def black_king_checked(board):
    # Find the position of the white king
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == "k":
                king_pos = row, col
                break
        if king_pos:
            break

    end = row, col

    # Check if any black piece can attack the white king
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            begin = row, col

            if piece.isupper():  # It's a white piece
                #print(piece, begin)

                if (piece == "P" and white_pawn_legal(begin, end, "white", board)) or \
                   (piece == "N" and knight_legal(begin, end, "white", board)) or \
                   (piece == "R" and rook_legal(begin, end, "white", board)) or \
                   (piece == "B" and bishop_legal(begin, end, "white", board)) or \
                   (piece == "Q" and queen_legal(begin, end, "white", board)) or \
                   (piece == "K" and king_legal(begin, end, "white", board)):
                    print(piece)
                    return True

    return False

def display_board(board):
    for row in board:
        print(" ".join(row))

