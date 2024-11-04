import chess
import chess.pgn
import random

def random_chess_game(messages):
    board = chess.Board()
    game = chess.pgn.Game()
    node = game

    # Loop until the game is over
    while not board.is_game_over():
        # Generate a list of all legal moves
        legal_moves = list(board.legal_moves)
        # Pick a random legal move
        move = random.choice(legal_moves)
        # Make the move on the board
        board.push(move)
        # Add the move to the PGN
        node = node.add_variation(move)

        # Add a message after the move if there are messages left
        if messages:
            comment = messages.pop(0)  # Get and remove the first message
            node.comment = comment     # Add the message as a comment

    # Set the game result
    if board.is_checkmate():
        game.headers["Result"] = "1-0" if board.turn == chess.BLACK else "0-1"
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        game.headers["Result"] = "1/2-1/2"  # Draw
    else:
        game.headers["Result"] = "*"

    return game

def save_pgn(game, filename="random_chess_game_with_messages.pgn"):
    # Save the PGN game to a file
    with open(filename, "w") as pgn_file:
        pgn_file.write(str(game))

if __name__ == "__main__":
    # Define a list of messages to add as comments after some moves
    messages = [
        "1",
        "2",
        "3",
        "4",
        "5"
    ]

    # Generate a random chess game with messages
    game = random_chess_game(messages)
    # Print the PGN to the console
    print(game)
    # Optionally save the game to a PGN file
    save_pgn(game)
