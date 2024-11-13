import chess

# ASCII Offset: make sure our computed values map to readable ASCII characters
ASCII_OFFSET = 32  # Start encoding from space in ASCII

# Encoding a message to chess moves based on target square's row and column
def encode_message_to_moves(board, message):
    moves = []

    # add chosen opening to the board here first before message
    
    for char in message:
        # Calculate ASCII code for character
        ascii_val = ord(char)
        ascii_adjusted = ascii_val - ASCII_OFFSET
        
        # Determine target square from ASCII value (Column and Row)
        col = (ascii_adjusted // 8) + 1  # Calculate column (1-8)
        row = (ascii_adjusted % 8) + 1  # Calculate row (1-8)
        
        # Convert column (1-8) to chess notation ('a'-'h')
        target_square = chess.square(col - 1, row - 1)
        
        # Find a legal move to the target square
        for pawn_square in range(chess.A2, chess.H2 + 1):
            if board.piece_at(pawn_square) == chess.Piece(chess.PAWN, chess.WHITE):
                move = chess.Move(pawn_square, target_square)
                if board.is_legal(move):
                    board.push(move)
                    moves.append(move)
                    break
                
    return moves

# Decoding moves back to message by analyzing the row and column of each move's target square
def decode_moves_to_message(board, moves):
    decoded_message = ""
    
    for move in moves:
        target_square = move.to_square
        col = chess.square_file(target_square) + 1
        row = chess.square_rank(target_square) + 1
        
        # Convert column and row back to ASCII
        ascii_val = ((col - 1) * 8) + (row - 1) + ASCII_OFFSET
        decoded_message += chr(ascii_val)
        
        # Make the move on the board (if needed for board consistency)
        board.push(move)
    
    return decoded_message

# Example usage
board = chess.Board()
message = "HELLO"
encoded_moves = encode_message_to_moves(board, message)
print("Encoded moves:", [board.san(move) for move in encoded_moves])

# Reset board for decoding
board = chess.Board()
decoded_message = decode_moves_to_message(board, encoded_moves)
print("Decoded message:", decoded_message)