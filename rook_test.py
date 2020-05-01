
import unittest
from server import rook

class RookTests(unittest.TestCase):
    def test_invalid_horizontal_movement_jump_from_piece(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            ['pw', None, None, None],  # 2
            ['rw', None, None, None],  # 3
        ]
        is_valid = rook(3, 0, 1, 0, board)
        self.assertEqual(is_valid, False)
    
    def test_invalid_vertical_movement_jump_from_piece(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            ['rw', 'rb', None, None],  # 3
        ]
        is_valid = rook(3, 0, 3, 2, board)
        self.assertEqual(is_valid, False)
    
    def test_invalid_movement_Diagonal(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            ['rw', None, None, None],  # 3
        ]
        is_valid = rook(3, 0, 1, 2, board)
        self.assertEqual(is_valid, False)
    
    def test_attack_enemy(self):
        board = [
            # 0     1     2     3
            ['rb', None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            ['rw', None, None, None],  # 3
        ]
        is_valid = rook(3, 0, 0, 0, board)
        self.assertEqual(is_valid, True)
