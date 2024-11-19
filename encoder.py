import chess
import chess.pgn
import binary_encoding
import lightvsdark
import moveToASCII

openings = {
    #"Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"], 
    "Sicilian Defense": ["e4", "c5", "Nf3", "d6"], # light vs dark binary
    "French Defense": ["e4", "e6", "d4", "d5"], # comment binary
    "Queen's Gambit": ["d4", "d5", "c4"], # move based ASCII
    #"King's Indian Defense": ["d4", "Nf6", "c4", "g6"],
}

def save_pgn(game):
    filename = input("Please enter a name for the file: ")
    filename = filename + ".pgn"
    # Save the PGN game to a file
    with open(filename, "w") as pgn_file:
        pgn_file.write(str(game))

if __name__ == "__main__":
    print("Available openings:")
    for i, opening in enumerate(openings.keys(), start=1):
        print(f"{i}.{opening}")
    choice = int(input("Select an opening by number (1-3): "))
    opening_choice = list(openings.keys())[choice - 1]
    message = input("Please input message to transmit: ")


    # Call function based on opening
    if opening_choice == "French Defense":
        game = binary_encoding.comment_encode(message) # works?
    if opening_choice == "Sicilian Defense":
        game = lightvsdark.encode_with_square_colors(message) # WIP
    if opening_choice == "Queen's Gambit":
        game = moveToASCII.encode_message_to_game(message) # the code for this one is superbly fucked right now

    #add code here to complete game after message is put into the game? Figure out what needs to be returned, game vs board?

    # Print game to console
    print(game)

    # Save game to pgn for upload
    if input("\nWould you like to save the game? y/n: ") == "y":
        save_pgn(game)