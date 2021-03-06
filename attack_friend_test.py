import unittest
from server import attack_friend

class AttackFriendTests(unittest.TestCase):
    def test_attack_friend(self):
        board = [
            # 0     1     2     3
            ['hw', None, None, None],  # 0
            [None, None, 'pw', None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, None],  # 3
        ]
        non_valid = attack_friend(0, 0, 1, 2, board)
        self.assertEqual(non_valid, True)

    def test_move_to_none(self):
        board = [
            # 0     1     2     3
            ['hw', None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, None],  # 3
        ]
        non_valid = attack_friend(0, 0, 2, 1, board)
        self.assertEqual(non_valid, False)
    
    def test_move_to_self(self):
        board = [
            # 0     1     2     3
            ['hw', None, None, None],  # 0
            [None, None, None, None],  # 1
            [None, None, None, None],  # 2
            [None, None, None, None],  # 3
        ]
        non_valid = attack_friend(0, 0, 0, 0, board)
        self.assertEqual(non_valid, True)
