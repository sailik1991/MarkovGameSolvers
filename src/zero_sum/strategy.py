import importlib
import numpy as np
from game import MTD_Game 
from utils import *

__author__ = "Sailik Sengupta"

class Strategy:
    def __init__(self, game_to_play=MTD_Game(), gamma=0.5):
        self.game = game_to_play
        self.DISCOUNT_FACTOR = gamma
        self.lib = importlib.import_module('gurobi')

    def set_gamma(self, gamma):
        self.DISCOUNT_FACTOR = gamma

    def initilize_V(self, S):
        V = {}
        for s in S:
            V[s] = 0
        return V

    def update_Q(self, S, A1, A2, R, T, V):
        Q = {}
        # Update the Q values for each state
        for s in S:
            for d in range(len(A1[s])):
                for a in range(len(A2[s])):
                    sda = '{}_{}_{}'.format(s, A1[s][d], A2[s][a])
                    Q[sda] = R[s][a][d]
                    for s_new in S:
                        Q[sda] += T[s][a][d][s_new] * self.DISCOUNT_FACTOR * V[s_new]
        return Q

    '''
    Given the new Q values, updates the optimal values for each state.
    Each agent type selects the implementation of this method.
    '''
    def get_value(self, s, A1, A2, R, T, Q):
       raise NotImplementedError

    def run(self):
        S  = self.game.get_S()
        A1 = self.game.get_A(1)
        A2 = self.game.get_A(0)
        R = self.game.get_R()
        T = self.game.get_T() 

        V = self.initilize_V(S) 

        for k in range(301):
            Q = self.update_Q(S, A1, A2, R, T, V)
           
            # Update Value function
            V_new = {}
            pi = {}
            for s in S:
                V_new[s], pi[s] = self.get_value(s, A1[s], A2[s], R[s], T[s], Q)
            V = V_new
            
            print_iteration_info(k, V, pi)
        return (V, pi)
