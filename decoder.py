import chess.pgn
import binary_encoding

openings = {
    #"Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"], 
    "Sicilian Defense": ["e4", "c5", "Nf3", "d6"], # light vs dark binary
    "French Defense": ["e4", "e6", "d4", "d5"], # comment binary
    "Queen's Gambit": ["d4", "d5", "c4"], # move based ASCII
    #"King's Indian Defense": ["d4", "Nf6", "c4", "g6"],
}

if __name__ == "__main__":
    filename = input("Please enter the name of the file (ex test.pgn): ")
    # add check here for specific openings in order to call specific decode functions
    message = binary_encoding.comment_decode(filename)
    print("Decoded Message: " + message)