import unittest
from server import attack_friend, bishop #translate_notation, http_move, attack_friend, pawn

    
class BishopTests(unittest.TestCase):
    def test_nobody_in_the_way(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, 'pb', None],  # 1
            [None, None, None, None],  # 2
            ['bw', None, None, None],  # 3
        ]
        is_valid = bishop(3, 0, 1, 2, board)
        self.assertEqual(is_valid, True)

    def test_somebody_in_the_way(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, 'pb', None],  # 1
            [None, 'hb', None, None],  # 2
            ['bw', None, None, None],  # 3
        ]
        is_valid = bishop(3, 0, 1, 2, board)
        self.assertEqual(is_valid, False)
    
    def test_wrong_movement(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            ['bw', None, None, None],  # 3
        ]
        is_valid = bishop(3, 0, 0, 0, board)
        self.assertEqual(is_valid, False)

    def test_two_empty_squares(self):
        board = [
            # 0     1     2     3
            [None, None, None, 'pb'],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            ['bw', None, None, None],  # 3
        ]
        is_valid = bishop(3, 0, 0, 3, board)
        self.assertEqual(is_valid, True)

    def test_jump_over_somebody(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, 'pb', None],  # 1
            [None, None, None, None],  # 2
            ['bw', None, None, None],  # 3
        ]
        is_valid = bishop(3, 0, 0, 3, board)
        self.assertEqual(is_valid, False)

#top left direction
    def test_jump_over_somebody_top_left(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, 'pb', None, None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, 'bw'],  # 3
        ]
        is_valid = bishop(0, 3, 0, 0, board)
        self.assertEqual(is_valid, False)

unittest.main()
