

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




def legal_moves(piece, begin, board):

    if board[begin[0]][begin[1]] != piece:
        return False

    lst = []

    for i in range(8):
        for j in range(8):
            end = (i, j)
            if legal_move(piece, begin, end, "a", board):      #chosen_figure, begin, end, color, board
                lst.append(end)

    return lst


def score_board(board):
    val = {"P":1, "R": 5, "B":3, "N":3, "Q": 9, "p":1, "r":5, "b":3, "n": 3, "q":9}
    sum_white = 0
    sum_black = 0

    for row in board:
        for piece in row:
            if piece.isupper() and piece != "K":
                sum_white += val[piece]

    for row in board:
        for piece in row:
            if piece.islower() and piece != "k":
                sum_black += val[piece]

    return sum_white - sum_black




def bestmove(board):
    best_score = float('inf')  # Initialize best_score to positive infinity for minimization
    best_move = None
    depth = 4  # Starting depth for the minimax search
    color = "black"

    board_copy = [row[:] for row in board]  # Deep copy of the board

    for i, row in enumerate(board_copy):
        for j, piece in enumerate(row):
            if piece.islower() and piece != ".":  # Only consider black pieces
                begin = (i, j)
                all_legal_moves = legal_moves(piece, begin, board_copy)

                for move in all_legal_moves:
                    # Simulate the move
                    board_copy[begin[0]][begin[1]] = "."
                    board_copy[move[0]][move[1]] = piece

                    # Call minimax to evaluate the move
                    score = minimax(board_copy, depth - 1, True)  # True indicates it's black's turn

                    # Update best_score and best_move based on the evaluation
                    if score < best_score:
                        best_score = score
                        best_move = (begin, move)
                        print(best_move)
                        print(best_score)
                        print()

                    # Revert the move
                    board_copy[begin[0]][begin[1]] = piece
                    board_copy[move[0]][move[1]] = "."

    return best_move

def minimax(board, depth, is_black_turn):
    if depth == 0:
        return score_board(board)  # Base case: return board evaluation

    if is_black_turn:
        best_score = float('inf')
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if piece.islower() and piece != ".":
                    begin = (i, j)
                    all_legal_moves = legal_moves(piece, begin, board)
                    for move in all_legal_moves:
                        # Simulate move
                        original_piece = board[move[0]][move[1]]
                        board[begin[0]][begin[1]] = "."
                        board[move[0]][move[1]] = piece
                        score = minimax(board, depth - 1, False)  # Next turn is white's
                        best_score = min(score, best_score)
                        # Revert move
                        board[begin[0]][begin[1]] = piece
                        board[move[0]][move[1]] = original_piece
        return best_score

    else:  # Now evaluating for white
        best_score = float('-inf')
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if piece.isupper() and piece != ".":
                    begin = (i, j)
                    all_legal_moves = legal_moves(piece, begin, board)
                    for move in all_legal_moves:
                        # Simulate move
                        original_piece = board[move[0]][move[1]]
                        board[begin[0]][begin[1]] = "."
                        board[move[0]][move[1]] = piece
                        score = minimax(board, depth - 1, True)  # Switch back to black's turn
                        best_score = max(score, best_score)
                        # Revert move
                        board[begin[0]][begin[1]] = piece
                        board[move[0]][move[1]] = original_piece
        return best_score


"""
board = [["."]*8 for _ in range(8)]
board[7] = ["R", "N", "B", ".", "K", "B", "N", "R"]
board[6] = ["P"]*8
board[0] = ["r", "n", "b", "q", "k", "b", "n", "r"]
board[1] = ["p"]*8
board[2][0] = "Q"
display_board(board)

print(bestmove(board))
begin, end = bestmove(board)
piece = board[begin[0]][begin[1]]

board[begin[0]][begin[1]] = "."

board[end[0]][end[1]] = piece

display_board(board)
#minimax(board)

#print(legal_moves("P", (6,7), "white", board))
"""