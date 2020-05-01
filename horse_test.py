import unittest
from server import horse, attack_friend

class HorseTests(unittest.TestCase):
    def test_horse_long_vertical(self):
        board = [
            # 0     1     2     3
            ['hw', None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, None],  # 3

        ]
        valid = horse(0, 0, 1, 2, board)
        self.assertEqual(valid, True)

    def test_horse_diagonal(self):
        board = [
            # 0     1     2     3
            ['hw', None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, None],  # 3

        ]
        valid = horse(0, 0, 1, 1, board)
        self.assertEqual(valid, False)
