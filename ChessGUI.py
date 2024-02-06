import tkinter as tk
from PIL import Image, ImageTk
import chess

"""define board for internal state"""
board = [["."]*8 for _ in range(8)]
board[7] = ["R", "N", "B", "Q", "K", "B", "N", "R"]
board[6] = ["P"]*8
board[0] = ["r", "n", "b", "q", "k", "b", "n", "r"]
board[1] = ["p"]*8
chess.display_board(board)


"""Create chessboard GUI"""

root = tk.Tk()

board_size = 8
square_size = 60

canvas = tk.Canvas(root, width=board_size*square_size, height=board_size*square_size)
canvas.pack()

# Draw the board
for row in range(board_size):
    for column in range(board_size):
        color = "white" if (row + column) % 2 == 0 else "gray"
        canvas.create_rectangle(column*square_size, row*square_size, column*square_size+square_size, row*square_size+square_size, fill=color)

# Load and place pawns
white_pawn = Image.open("LightPawn.webp")
white_pawn_resized = white_pawn.resize((square_size, square_size))  # Resize the image to fit within a square
white_pawn = ImageTk.PhotoImage(white_pawn_resized)

for i in range(board_size):
    canvas.create_image(i*square_size, 6*square_size, anchor=tk.NW, image= white_pawn, tags = "piece")


#Same for black pawns
black_pawn = Image.open("DarkPawn.webp")
black_pawn_resized = black_pawn.resize((square_size, square_size))  # Resize the image to fit within a square
black_pawn = ImageTk.PhotoImage(black_pawn_resized)

for i in range(board_size):
    canvas.create_image(i*square_size, 1*square_size, anchor=tk.NW, image= black_pawn, tags = "piece")


image_references = []

def put_on_chessboard(column, row, name):
    global image_references
    piece = Image.open(name)
    piece_resized = piece.resize((square_size, square_size))
    piece_photo = ImageTk.PhotoImage(piece_resized)
    # Store the reference to prevent garbage collection
    image_references.append(piece_photo)
    canvas.create_image(column * square_size, row * square_size, anchor=tk.NW, image=piece_photo, tags="piece")


put_on_chessboard(1, 7, "LightKnight.webp")
put_on_chessboard(6, 7, "LightKnight.webp")
put_on_chessboard(1, 0, "DarkKnight.webp")
put_on_chessboard(6, 0, "DarkKnight.webp")
put_on_chessboard(0, 7, "LightRook.webp")
put_on_chessboard(7, 7, "LightRook.webp")
put_on_chessboard(0, 0, "DarkRook.webp")
put_on_chessboard(7, 0, "DarkRook.webp")
put_on_chessboard(2, 7, "LightBishop.webp")
put_on_chessboard(5, 7, "LightBishop.webp")
put_on_chessboard(2, 0, "DarkBishop.webp")
put_on_chessboard(5, 0, "DarkBishop.webp")
put_on_chessboard(3, 7, "LightQueen.webp")
put_on_chessboard(3, 0, "DarkQueen.webp")
put_on_chessboard(4, 7, "LightKing.webp")
put_on_chessboard(4, 0, "DarkKing.webp")


# Initialize variables for tracking figure selection
figure_selected = False
selected_figure_id = None
selected_figure_position = (None, None)
chosen_figure = None
begin = None
white = True


def handle_click(event):
    global figure_selected, selected_figure_id, chosen_figure, begin, board, white

    clicked_row = event.y // square_size
    clicked_column = event.x // square_size


    if not figure_selected:                                                   #first click, so nothing is selected
        chosen_figure = board[clicked_row][clicked_column]                          #find what user clicked on
        if chosen_figure != ".":

            figure_selected = True
            begin = (clicked_row, clicked_column)  # Save the beginning position
            selected_figure_id = canvas.find_closest(event.x, event.y)[0]  # Find and save the ID of the clicked pawn
    else:
        end = (clicked_row, clicked_column)  # Save the end position

        #white plays
        if chess.legal_move(chosen_figure, begin, end, color, board) and board[begin[0]][begin[1]].isupper() and white == True:

            board_temp = [row[:] for row in board]
            board_temp[begin[0]][begin[1]] = "."
            board_temp[end[0]][end[1]] = chosen_figure

            if not chess.white_king_checked(board_temp):
                # Calculate movement for the figure
                board[begin[0]][begin[1]] = "."
                board[end[0]][end[1]] = chosen_figure


                dx = (end[1] - begin[1]) * square_size
                dy = (end[0] - begin[0]) * square_size

                # Calculate the square's coordinates on the canvas
                top_left_x = end[1] * square_size
                top_left_y = end[0] * square_size
                bottom_right_x = top_left_x + square_size
                bottom_right_y = top_left_y + square_size

                # Check for any items in the target square
                items_in_square = canvas.find_overlapping(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
                for item_id in items_in_square:
                    if "piece" in canvas.gettags(item_id) and item_id != selected_figure_id:
                        canvas.delete(item_id)

                # Move the figure on the canvas
                canvas.move(selected_figure_id, dx, dy)

                # Update the internal board representation
                board[begin[0]][begin[1]] = "."
                board[end[0]][end[1]] = chosen_figure


                # Reset selection variables
                figure_selected = False
                chosen_figure = None
                begin = None

                #and now it is black's turn
                white = False

                #chess.display_board(board)
            else:
                print("i dont think so!")
                figure_selected = False
                chosen_figure = None
                begin = None

        #black plays
        elif chess.legal_move(chosen_figure, begin, end, color, board) and board[begin[0]][begin[1]].islower() and white == False:
            board_temp = [row[:] for row in board]
            board_temp[begin[0]][begin[1]] = "."
            board_temp[end[0]][end[1]] = chosen_figure

            if not chess.black_king_checked(board_temp):
                # Calculate movement for the figure
                board[begin[0]][begin[1]] = "."
                board[end[0]][end[1]] = chosen_figure

                dx = (end[1] - begin[1]) * square_size
                dy = (end[0] - begin[0]) * square_size

                # Calculate the square's coordinates on the canvas
                top_left_x = end[1] * square_size
                top_left_y = end[0] * square_size
                bottom_right_x = top_left_x + square_size
                bottom_right_y = top_left_y + square_size

                # Check for any items in the target square
                items_in_square = canvas.find_overlapping(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
                for item_id in items_in_square:
                    if "piece" in canvas.gettags(item_id) and item_id != selected_figure_id:
                        canvas.delete(item_id)

                # Move the figure on the canvas
                canvas.move(selected_figure_id, dx, dy)

                # Update the internal board representation
                board[begin[0]][begin[1]] = "."
                board[end[0]][end[1]] = chosen_figure

                # Reset selection variables
                figure_selected = False
                chosen_figure = None
                begin = None

                # and now it is white's turn
                white = True

                # chess.display_board(board)
            else:
                print("i dont think so!")
                figure_selected = False
                chosen_figure = None
                begin = None




def cancel_choice(event):
    global chosen_figure, begin, figure_selected

    print("cc")
    figure_selected = False
    chosen_figure = None
    begin = None

# Bind the click event to the canvas

canvas.bind("<Button-1>", handle_click)
canvas.bind("<Button-3>", cancel_choice)

root.mainloop()
