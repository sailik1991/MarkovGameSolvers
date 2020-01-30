import importlib
import numpy as np
from game import GeneralSum_Game 
from utils import *

__author__ = "Sailik Sengupta"

class Strategy:
    def __init__(self, game_to_play=GeneralSum_Game(), gamma=0.5):
        self.game = game_to_play
        self.DISCOUNT_FACTOR = gamma
        self.lib = importlib.import_module('gurobi')

    def set_gamma(self, gamma):
        self.DISCOUNT_FACTOR = gamma

    def initialize_V(self, S):
        V = {}
        for s in S:
            V[s] = 0
        return V

    def update_Q(self, S, A_D, A_A, R_D, R_A, T, V_D, V_A):
        Q_D = {}
        Q_A = {}
        # Update the Q values for each state
        for s in S:
            '''
            print('--- {} ---'.format(s))
            print(R_D[s])
            print(R_A[s])
            print()
            '''

            for d in range(len(A_D[s])):
                for a in range(len(A_A[s])):
                    sda = '{}_{}_{}'.format(s, A_D[s][d], A_A[s][a])
                    Q_D[sda] = R_D[s][a][d]
                    Q_A[sda] = R_A[s][a][d]
                    for s_new in S:
                        Q_D[sda] += T[s][a][d][s_new] * self.DISCOUNT_FACTOR * V_D[s_new]
                        Q_A[sda] += T[s][a][d][s_new] * self.DISCOUNT_FACTOR * V_A[s_new]
        return (Q_D, Q_A)

    '''
    Given the new Q values, updates the optimal values for each state.
    Each agent type selects the implementation of this method.
    '''
    def get_value(self, s, A_D, A_A, R_D, R_A, T, Q_D, Q_A):
       raise NotImplementedError

    def run(self):
        S  = self.game.get_S()
        A_D = self.game.get_A(1)
        A_A = self.game.get_A(0)
        R_D = self.game.get_R(1)
        R_A = self.game.get_R(0)
        T = self.game.get_T() 

        V_D = self.initialize_V(S)
        V_A = self.initialize_V(S)

        for k in range(10):
            Q_D, Q_A = self.update_Q(S, A_D, A_A, R_D, R_A, T, V_D, V_A)
           
            # Update Value function
            V_D_new = {}
            V_A_new = {}
            pi = {}
            for s in S:
                V_D_new[s], V_A_new[s], pi[s] = self.get_value(s, A_D[s], A_A[s], R_D[s], R_A[s], T[s], Q_D, Q_A)
            V_D = V_D_new
            V_A = V_A_new
            
            #print_iteration_info(k, V, pi)
        return (V_D, pi)
