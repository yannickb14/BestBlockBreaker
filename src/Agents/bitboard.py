



class BitboardSimulator:
    def __init__(self, board_list=None): 
        #self.board = 0
        self.ROW_MASKS = [(0b1111111111 << (r * 10)) for r in range(10)]
        self.COL_MASKS = [sum(1 << (r * 10 + c) for r in range(10)) for c in range(10)]

        self.ROW_0_MASK = 0b1111111111                  # First row
        self.ROW_9_MASK = 0b1111111111 << 90            # Last row
        self.COL_0_MASK = sum(1 << (r * 10) for r in range(10))      # First col
        self.COL_9_MASK = sum(1 << (r * 10 + 9) for r in range(10))  # Last col

        self.NOT_COL_0 = ~self.COL_0_MASK
        self.NOT_COL_9 = ~self.COL_9_MASK

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

    
    # <---- HEURISTICS ---->

    def count_empty_cells(self):
        # A simple hole count (empty cells)
        occupied = self.board.bit_count() 
        return 100 - occupied

    def count_isolated_holes(self):
        """
        Counts 1x1 empty spots completely surrounded by blocks or walls.
        """
        b = self.board

        # 1. Check Left Neighbor
        # Shift board LEFT (<< 1). 
        # Must mask out Col 9 first so it doesn't wrap to Col 0 of next row.
        # OR with COL_0_MASK because the left wall acts as a "block".
        left_filled = ((b & self.NOT_COL_9) << 1) | self.COL_0_MASK

        # 2. Check Right Neighbor
        # Shift board RIGHT (>> 1).
        # Must mask out Col 0 first.
        # OR with COL_9_MASK because the right wall acts as a "block".
        right_filled = ((b & self.NOT_COL_0) >> 1) | self.COL_9_MASK

        # 3. Check Up Neighbor
        # Shift board UP (<< 10). 
        # OR with ROW_0 because the top wall acts as a "block".
        up_filled = (b << 10) | self.ROW_0_MASK

        # 4. Check Down Neighbor
        # Shift board DOWN (>> 10).
        # OR with ROW_9 because the bottom wall acts as a "block".
        down_filled = (b >> 10) | self.ROW_9_MASK

        # 5. Combine
        # A spot is "surrounded" if ALL 4 neighbors are filled (AND operator)
        surrounded = left_filled & right_filled & up_filled & down_filled

        # 6. Find the Holes
        # We only care about spots that are currently EMPTY (~b)
        # AND are surrounded
        isolated_holes = surrounded & ~b

        # Return the count
        return isolated_holes.bit_count()
        
        