__author__ = "Sailik Sengupta"

class MTD_Game(object):
    def __init__(self):
        self.S = [0, 1, 2, 3]

        self.A = [
            # Row player (Attacker) actions corresponding to each state
            [
	        ['success'],  #exploit success
                ['no-op', 'exp-ipfire'], #Attacker outside n/w 
                ['no-op', 'exp-win12', 'exp-win7', 'exp-ftp', 'exp-dns'], # Attacker on fw 
                ['no-op', 'exp-ftp'], #attacker on Win 12
            ],
            # Column player (Defender) actions corresponding to each state
            [
                ['lost'],
                ['no-mon', 'mon-ipfire'],
                ['no-mon', 'mon-win12', 'mon-win7', 'mon-ftp', 'mon-dns'],
                ['no-mon', 'mon-ftp'],
            ]
        ]

        # R(s, a1, a2)
        self.R = [
            [
                [-20]
            ],
            [
                [0, -3],
                [-6.8, 10]
            ],
            [
                [0, -3, -3, -5, -5],
                [-5, 5, -3, -5, -5],
                [-5, -3, 5, -5, -5],
		[-10, -3, -3,  10, -5],
		[-10, -3, -3, -5, 10]
				
            ],
            [
                [0, -3],
                [-0, 20]
            ]
        ]

        # T(s, a1, a2, s')
        self.T = [
            [
                [(1, 0, 0, 0)]
            ],
           
            [
                [(0, 1, 0, 0), (0, 1, 0, 0)],
                [(0, 0.32, 0.68, 0), (0, 0.9, 0.1, 0)]
            ],
            [
                [(0, 0, 1, 0), (0, 0, 1, 0), (0, 0, 1, 0),  (0, 0, 1, 0), (0, 0, 1, 0)],
                [(0, 0, 0.3, 0.7), (0.8, 0, 0.1, 0.1), (0.2, 0, 0.2, 0.6),  (0, 0, 0.3, 0.7), (0, 0, 0.3, 0.7)],
                [(0, 0, 0.3, 0.7), (0.4, 0, 0.4, 0.3), (0.8, 0, 0.1, 0.1),  (0, 0, 0.3, 0.7), (0, 0, 0.3, 0.7)],
                [(0, 0, 0.4, 0.6), (0.5, 0.1, 0.1, 0.2), (0, 0, 0.4, 0.6),  (0.8, 0, 0.1, 0.1), (0, 0, 0.4, 0.6)],
                [(0, 0, 0.4, 0.6), (0.5, 0.1, 0.1, 0.2), (0, 0, 0.4, 0.6),  (0, 0, 0.4, 0.6), (0.8, 0, 0.1, 0.1)],
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
