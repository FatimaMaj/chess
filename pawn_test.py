import unittest
from server import pawn

class PawnTests(unittest.TestCase):
    def test_pawn_two_steps_forward(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'pw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        valid = pawn(2, 1, 0, 1, board)
        self.assertEqual(valid, True)

    def test_white_attack_competitor(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, 'pb', None],  # 1
            [None, 'pw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        valid = pawn(2, 1, 1, 2, board)
        self.assertEqual(valid, True)

    def test_white_attack_friend(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, 'pw', None],  # 1
            [None, 'pw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        valid = pawn(2, 1, 1, 2, board)
        self.assertEqual(valid, False)
    
    def test_white_pawn_backwards(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'pw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        valid = pawn(2, 1, 3, 1, board)
        self.assertEqual(valid, False)
    
    def test_white_pawn_two_steps_not_straight(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'pw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        valid = pawn(2, 1, 0, 3, board)
        self.assertEqual(valid, False)
    
    def test_black_pawn_two_steps_not_straight(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, 'pb', None, None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, None],  # 3
        ]
        valid = pawn(1, 1, 3, 3, board)
        self.assertEqual(valid, False)
    
    def test_black_pawn_one_step(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, 'pb', None, None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, None],  # 3
            [None, None, None, None],  # 4
            [None, 'hw', None, None],  # 5
        ]
        valid = pawn(1, 1, 2, 1, board)
        self.assertEqual(valid, True)
    
    def test_black_pawn_two_steps(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, 'pb', None, None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, None],  # 3
            [None, None, None, None],  # 4
            [None, 'hw', None, None],  # 5
        ]
        valid = pawn(1, 1, 3, 1, board)
        self.assertEqual(valid, True)
