import unittest
from server import queen

class queenTest(unittest.TestCase):

    def test_queen_as_rook(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            ['qw', None, None, None],  # 3
        ]
        is_valid = queen(3, 0, 0, 0, board)
        self.assertEqual(is_valid, True)

    def test_queen_as_boshop(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            ['qw', None, None, None],  # 3
        ]
        is_valid = queen(3, 0, 0, 3, board)
        self.assertEqual(is_valid, True)
unittest.main()