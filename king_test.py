import unittest
from server import king

class KingTest(unittest.TestCase):
    def test_attack_right_side(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 2, 2, 'white', board)
        self.assertEqual(is_valid, True)

    def test_attack_bottom_right(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 3, 2, 'white', board)
        self.assertEqual(is_valid, True)
    
    def test_attack_bottom(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 3, 1, 'white', board)
        self.assertEqual(is_valid, True)
    
    def test_attack_bottom_left(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 3, 0, 'white', board)
        self.assertEqual(is_valid, True)
    
    def test_attack_left(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 2, 0, 'white', board)
        self.assertEqual(is_valid, True)

    def test_attack_top_left(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 1, 0, 'white', board)
        self.assertEqual(is_valid, True)
    
    def test_attack_top(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 1, 1, 'white', board)
        self.assertEqual(is_valid, True)

    def test_attack_top_right(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, None, None, None],  # 3
        ]
        is_valid = king(2, 1, 1, 2, 'white', board)
        self.assertEqual(is_valid, True)

    def test_horse_attack_king(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kw', None, None],  # 2
            [None, 'hb', None, None],  # 3
        ]
        is_valid = king(2, 1, 1, 2, 'white', board)
        self.assertEqual(is_valid, False)
    
    def test_horse_pawn_attack_king(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kb', None, 'pw'],  # 2
            [None, 'hw', None, None],  # 3
        ]
        is_valid = king(2, 1, 1, 2, 'black', board)
        self.assertEqual(is_valid, False)
    
    def test_one_of_two_can_attack_king(self):
        board = [
            # 0     1     2     3
            [None, None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kb', None, None],  # 2
            [None, 'hw', None, 'pw'],  # 3
        ]
        is_valid = king(2, 1, 1, 2, 'black', board)
        self.assertEqual(is_valid, False)
    
    def test_multiple_enemy_without_attacking_king(self):
        board = [
            # 0     1     2     3
            ['qw', None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, 'kb', None, None],  # 2
            ['hw', None, None, 'pw'],  # 3
        ]
        is_valid = king(2, 1, 1, 2, 'black', board)
        self.assertEqual(is_valid, True)

unittest.main()