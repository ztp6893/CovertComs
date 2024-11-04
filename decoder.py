import chess.pgn

def extract_comments_from_pgn(filename):
    comments = []

    # Open the PGN file and parse each game
    with open(filename, "r") as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # End of file

            # Traverse through each move in the game
            node = game
            while node.variations:
                node = node.variation(0)  # Move to the next node
                if node.comment:
                    comments.append(node.comment)

    # Combine all comments into a single string
    all_comments = " ".join(comments)
    return all_comments

if __name__ == "__main__":
    # Replace 'random_chess_game_with_comments.pgn' with your PGN file name
    filename = "random_chess_game_with_messages.pgn"
    all_comments = extract_comments_from_pgn(filename)
    
    # Print the combined comments
    print("Combined Comments:")
    print(all_comments)