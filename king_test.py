import unittest
from server import king

class queenTest(unittest.TestCase):

    def test_attack_right_side(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 2, 2, board)
        self.assertEqual(is_valid, True)

    def test_attack_bottom_right(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 3, 2, board)
        self.assertEqual(is_valid, True)
    
    def test_attack_bottom(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 3, 1, board)
        self.assertEqual(is_valid, True)
    
    def test_attack_bottom_left(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 3, 0, board)
        self.assertEqual(is_valid, True)
    
    def test_attack_left(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 2, 0, board)
        self.assertEqual(is_valid, True)

    def test_attack_top_left(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 1, 0, board)
        self.assertEqual(is_valid, True)
    
    def test_attack_top(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 1, 1, board)
        self.assertEqual(is_valid, True)

    def test_attack_top_right(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 1, 2, board)
        self.assertEqual(is_valid, True)
unittest.main()