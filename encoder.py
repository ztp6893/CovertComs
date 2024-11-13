import chess
import chess.pgn
import random
import binary_encoding
import lightvsdark
import moveToASCII

openings = {
    "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"], 
    "Sicilian Defense": ["e4", "c5", "Nf3", "d6"], # light vs dark binary
    "French Defense": ["e4", "e6", "d4", "d5"], # comment binary
    "Queen's Gambit": ["d4", "d5", "c4"], # move based ASCII
    "King's Indian Defense": ["d4", "Nf6", "c4", "g6"],
}

if __name__ == "__main__":
    print("Available openings:")
    for i, opening in enumerate(openings.keys(), start=1):
        print(f"{i}. {opening}")
    choice = int(input("Select an opening by number (1-5): "))
    opening_choice = list(openings.keys())[choice - 1]

    # Call function based on opening
    if opening_choice == "French Defense":
        message = input("Please input message to transmit: ")
        game = binary_encoding.comment_encode(message)