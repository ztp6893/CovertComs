import chess
import chess.pgn
import random

# Define some common openings
openings = {
    "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"],
    "Sicilian Defense": ["e4", "c5", "Nf3", "d6"],
    "French Defense": ["e4", "e6", "d4", "d5"],
    "Queen's Gambit": ["d4", "d5", "c4"],
    "King's Indian Defense": ["d4", "Nf6", "c4", "g6"],
}

def random_chess_game(messages, opening_choice):
    board = chess.Board()
    game = chess.pgn.Game()
    node = game

    # Play the selected opening
    if opening_choice in openings:
        opening_moves = openings[opening_choice]
        for move_san in opening_moves:
            move = board.parse_san(move_san)  # Parse the move in SAN notation
            board.push(move)                  # Make the move on the board
            node = node.add_variation(move)   # Add the move to the PGN

            # Add a message if available
            if messages:
                comment = messages.pop(0)
                node.comment = comment

    # Continue with random moves after the opening
    while not board.is_game_over():
        # Generate a list of all legal moves
        legal_moves = list(board.legal_moves)
        # Pick a random legal move
        move = random.choice(legal_moves)
        # Make the move on the board
        board.push(move)
        # Add the move to the PGN
        node = node.add_variation(move)

        # Add a message if available
        if messages:
            comment = messages.pop(0)
            node.comment = comment

    # Set the game result
    if board.is_checkmate():
        game.headers["Result"] = "1-0" if board.turn == chess.BLACK else "0-1"
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        game.headers["Result"] = "1/2-1/2"  # Draw
    else:
        game.headers["Result"] = "*"

    return game

def save_pgn(game, filename="random_chess_game_with_opening.pgn"):
    # Save the PGN game to a file
    with open(filename, "w") as pgn_file:
        pgn_file.write(str(game))

if __name__ == "__main__":
    # Define a list of messages to add as comments after moves
    messages = [
        "1",
        "2",
        "3",
        "4",
        "5"
    ]

    # Display available openings and let the user select one
    print("Available openings:")
    for i, opening in enumerate(openings.keys(), start=1):
        print(f"{i}. {opening}")
    choice = int(input("Select an opening by number (1-5): "))
    opening_choice = list(openings.keys())[choice - 1]

    # Generate a random chess game with the chosen opening
    game = random_chess_game(messages, opening_choice)
    # Print the PGN to the console
    print(game)
    # Optionally save the game to a PGN file
    save_pgn(game)