



class BitboardSimulator:
    def __init__(self, board_list=None): 
        #self.board = 0
        self.ROW_MASKS = [(0b1111111111 << (r * 10)) for r in range(10)]
        self.COL_MASKS = [sum(1 << (r * 10 + c) for r in range(10)) for c in range(10)]
        if board_list:
            self.board = self._list_to_bitboard(board_list)

    def _list_to_bitboard(self, board_list):
        bb = 0
        for r in range(10):
            for c in range(10):
                if board_list[r][c]:
                    index = (r * 10) + c
                    bb |= (1 << index)
        return bb

    def check_collision(self, piece_mask, offset_row, offset_col):
        # Calculate the shift required to move the piece to (row, col)
        shift = (offset_row * 10) + offset_col
        
        # Create the moved piece
        moved_piece = piece_mask << shift
        
        # Check if it overlaps with existing blocks
        if (self.board & moved_piece) != 0:
            return True # Collision!
            
        return False

    def place_piece(self, piece_mask, offset_row, offset_col):
        shift = (offset_row * 10) + offset_col
        self.board |= (piece_mask << shift)
        
    def clear_full_lines(self):
        # Identify full rows
        full_rows_mask = 0
        lines_cleared = 0
        
        for r_mask in self.ROW_MASKS:
            if (self.board & r_mask) == r_mask:
                full_rows_mask |= r_mask
                lines_cleared += 1

        # Identify full cols
        for c_mask in self.COL_MASKS:
            if (self.board & c_mask) == c_mask:
                full_rows_mask |= c_mask
                lines_cleared += 1
        
        # Remove them (XOR toggles the bits from 1 to 0)
        # We use XOR because we know for a fact they are all 1s.
        if lines_cleared > 0:
            self.board ^= full_rows_mask
            
        return lines_cleared

    # --- Heuristics for your Genetic Algorithm ---
    
    def get_number_of_holes(self):
        # A simple hole count (empty cells)
        # Use python's native optimized bit_count if available (Python 3.10+)
        occupied = self.board.bit_count() 
        return 100 - occupied
        
    def get_bumpiness(self):
        # Calculate how "rough" the top surface is (sum of height differences)
        # This requires iterating columns, but it's still fast operations
        total_bumpiness = 0
        prev_height = None
        
        for c in range(10):
            # Find height of this column
            col_mask = self.COL_MASKS[c]
            col_bits = self.board & col_mask
            
            # Simple way to get height: find the highest set bit in this column
            # (Math trickery can optimize this, but loop is fine for now)
            height = 0
            if col_bits > 0:
                # We can approximate or iterate. 
                # For exact height, we look for the highest index.
                # Since 1010! isn't gravity-based like Tetris, "Height" 
                # might actually mean "Row Index of lowest empty spot".
                # Adjust this heuristic based on your game rules.
                pass 
        return total_bumpiness