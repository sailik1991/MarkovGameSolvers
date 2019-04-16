__author__ = "Sailik Sengupta"

class MTD_Game(object):
    def __init__(self):
        self.S = [0, 1, 2, 3]

        self.A = [
            # Row player (Attacker) actions corresponding to each state
            [
                ['success'],
                ['no-op', 'exp-LDAP'],
                ['no-op', 'exp-Web', 'exp-FTP'],
                ['no-op', 'exp-FTP'],
            ],
            # Column player (Defender) actions corresponding to each state
            [
                ['lost'],
                ['no-mon', 'mon-LDAP'],
                ['no-mon', 'mon-Web', 'mon-FTP'],
                ['no-mon', 'mon-FTP'],
            ]
        ]

        # R(s, a1, a2)
        self.R = [
            [
                [-20]
            ],
            [
                [0, -3],
                [-5, 5]
            ],
            [
                [0, -2, -3],
                [-7, 5, -9],
                [-10, -10, 7]
            ],
            [
                [0, -2],
                [-10, 8]
            ]
        ]

        # T(s, a1, a2, s')
        self.T = [
            [
                [(1, 0, 0, 0)]
            ],
            [
                [(0, 1, 0, 0), (0, 1, 0, 0)],
                [(0, 0.5, 0.5, 0), (0, 0.9, 0.1, 0)]
            ],
            [
                [(0, 0, 1, 0), (0, 0, 1, 0), (0, 0, 1, 0)],
                [(0, 0, 0.3, 0.7), (0, 0.3, 0.1, 0.6), (0, 0, 0.4, 0.6)],
                [(0, 0, 0.4, 0.6), (0, 0, 0.3, 0.7), (0, 0.5, 0.1, 0.4)],
            ],
            [
                [(0, 0, 0, 1), (0, 0, 0, 1)],
                [(0.8, 0, 0, 0.2), (0.4, 0.4, 0, 0.2)]
            ]
        ]

    def get_S(self):
        return self.S

    def get_A(self, player):
        return self.A[player]

    def get_R(self):
        return self.R

    def get_T(self):
        return self.T

