import unittest
from GameLogic import GameLogic  
from Move import Move            

TEST_PIECE_DOT = [(0, 0)] 
TEST_PIECE_LINE_HORIZENTAL = [(0, 0), (0, 1), (0, 2)]
TEST_PIECE_LINE_VERTICAL = [(0,0), (1,0), (2,0)]

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        """
        Runs before EVERY single test function.
        Gives us a fresh game board each time.
        """

        self.game = GameLogic(10)
        self.game.displayed = [TEST_PIECE_DOT, TEST_PIECE_LINE_HORIZENTAL, TEST_PIECE_LINE_VERTICAL] #To get predictable states

    def test_initialization(self):
        """
        Check if the board starts empty and score is 0
        """
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.board), 10)
        
        self.assertEqual(self.game.board[5][5], 0)

    def test_valid_move(self):
        """
        Test placing a piece in an empty spot
        """
        
        move = Move(0, (5, 5)) #The dot
        
        #First move should be valid
        self.assertTrue(self.game.is_valid_move(move))

        #Test edge/corner moves
        move_corner = Move(0, (9, 9))
        move_edge = Move(0, (5, 9))
        
        self.assertTrue(self.game.is_valid_move(move_corner))
        self.assertTrue(self.game.is_valid_move(move_edge))

        self.game.execute_move(move)
        
        self.assertEqual(self.game.board[5][5], 1)

    def test_overlap_collision(self):
        """
        Test that we cannot place a piece on top of another
        """

        self.game.board[3][3] = 1

        move = Move(0, (3, 3))

        self.assertFalse(self.game.is_valid_move(move))

    def test_out_of_bounds(self):
        """
        Test placing a piece off the edge
        """
        
        move = Move(0, (10, 10))
        self.assertFalse(self.game.is_valid_move(move))

        move = Move(1, (9, 9))
        self.assertFalse(self.game.is_valid_move(move))

    def test_need_to_clear_row(self):
        """Test need to clear catches rows"""
        for c in range(10):
            self.game.board[9][c] = 1
        
        self.assertTrue(all(self.game.board[9]))

        rows_to_clear, cols_to_clear = self.game.need_to_clear()

        self.assertEqual(rows_to_clear, [9])
        self.assertEqual(cols_to_clear, [])
        
    def test_need_to_clear_col(self):
        '''Test need_to_clear catches columns'''
        for c in range(10):
            self.game.board[c][5] = 1

        for i in range(10):
            self.assertTrue(self.game.board[i][5])
        
        rows_to_clear, cols_to_clear = self.game.need_to_clear()

        self.assertEqual(rows_to_clear, [])
        self.assertEqual(cols_to_clear, [5])

    def test_execute_move_clears_row(self):
        '''
        Test that rows get cleared when executing a move
        and that score increments properly
        '''
        
        #Fill up a row except for one piece then
        #call execute move to place the one piece missing
        #and check that it clears and increments the score
        #properly
        for i in range(9):
            self.game.board[7][i] = 1
        
        move = Move(0, (7,9))
        self.game.execute_move(move)
        
        self.assertEqual(self.game.score, 11) #+10 for clearing +1 for placing 1x1 
        self.assertFalse(any(self.game.board[7]))

    def test_execute_move_clears_col(self):
        '''
        Test cols get cleared when executing a move
        and that score increments properly
        '''
        for i in range(9):
            self.game.board[i][8] = 1
        
        move = Move(0, (9,8))
        self.game.execute_move(move)
        
        self.assertEqual(self.game.score, 11) 
        for i in range(10):
            self.assertFalse(self.game.board[i][8])

    def test_execute_mult_rows_cols(self):
        '''
        Tests a more complex game scenario
        where many rows and columns are cleared
        at once.

        Note: If clearing a row and column at the same time,
        the game awards 10 for the row and 10 for the column
        even though one things gets cleared twice (the point of intersection of the row and column)
        '''
        #========================
        #Clear three cols at once
        #========================
        for row in range(5,8):
            for col in range(9):
                self.game.board[row][col] = 1

        move = Move(2, (5,9))
        self.assertTrue(self.game.is_valid_move(move))
        self.game.execute_move(move)
        for row in self.game.board:
            self.assertFalse(any(row))

        self.assertEqual(self.game.score, 33)

        #========================
        #Clear three rows at once
        #========================
        for row in range(9):
            for col in range(5,8):
                self.game.board[row][col] = 1

        move = Move(1, (9,5))
        self.assertTrue(self.game.is_valid_move(move))
        self.game.execute_move(move)
        for row in self.game.board:
            self.assertFalse(any(row))

        self.assertEqual(self.game.score, 66)

        #====================================
        #Clear a row and col at the same time
        #====================================
        for i in range (10):
            if i == 7:
                self.game.board[7][i] = 1
            elif i == 3:
                self.game.board[i][3] = 1
            else:
                self.game.board[7][i] = 1
                self.game.board[i][3] = 1

        #Place 1x1 piece at the intersection. Score should by 21
        move = Move(0, (7, 3))
        self.assertTrue(self.game.is_valid_move(move)) 
        self.game.execute_move(move)
        self.assertEqual(self.game.score, 87)



if __name__ == "__main__":
    unittest.main()


'''

'''