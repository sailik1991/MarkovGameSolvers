import numpy as np
import nashpy as nash
import warnings
from .strategy import Strategy

# Suppress nashpy warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

__author__ = "Sailik Sengupta"

class UniformRandom(Strategy):
    def get_name(self):
        return 'UR'

    def get_value(self, s, A_D, A_A, R_D, R_A, T, Q_D, Q_A):
        num_d = len(A_D)
        num_a = len(A_A)

        # Get Defender/Leader's Q-value matrix
        M_D = []
        M_A = []
        for d in range(num_d):
            row_D = []
            row_A = []
            for a in range(num_a):
                k = '{}_{}_{}'.format(s, A_D[d], A_A[a])
                row_D.append( Q_D[k] )
                row_A.append( Q_A[k] )
            M_D.append(row_D)
            M_A.append(row_A)

        g = nash.Game(M_D, M_A)
        
        D_s = [1.0/num_d for i in range(num_d)]
        game_value = [-10000,-10000]
        U_A = -100
        for a in range(num_a):
            A_s = [0 for i in range(num_a)]
            A_s[a] = 1.0
            U = g[D_s, A_s]
            if U[1] > game_value[1]:
                game_value = U

        policy = {}
        for d in range(num_d):
            policy['pi_{}'.format(A_D[d])] = D_s[d]

        return game_value[0], game_value[1], policy

class NashEq(Strategy):
    def get_name(self):
        return 'NE'

    def get_value(self, s, A_D, A_A, R_D, R_A, T, Q_D, Q_A):
        num_d = len(A_D)
        num_a = len(A_A)

        # Get Defender/Leader's Q-value matrix
        M_D = []
        M_A = []
        for d in range(num_d):
            row_D = []
            row_A = []
            for a in range(num_a):
                k = '{}_{}_{}'.format(s, A_D[d], A_A[a])
                row_D.append( Q_D[k] )
                row_A.append( Q_A[k] )
            M_D.append(row_D)
            M_A.append(row_A)

        g = nash.Game(M_D, M_A)
        try:
            # Try support enumeration first
            equilibria = list(g.support_enumeration())
            if equilibria:
                D_s, A_s = equilibria[0]
            else:
                # If no equilibria found, try lemke_howson
                equilibria = list(g.lemke_howson_enumeration())
                if equilibria:
                    D_s, A_s = equilibria[0]
                else:
                    # If still no equilibria, use uniform random strategy
                    D_s = np.array([1.0/num_d for _ in range(num_d)])
                    A_s = np.array([1.0/num_a for _ in range(num_a)])
        except (IndexError, Exception) as e:
            # Fallback to uniform random strategy
            D_s = np.array([1.0/num_d for _ in range(num_d)])
            A_s = np.array([1.0/num_a for _ in range(num_a)])
            
        game_value = g[D_s, A_s]

        policy = {}
        for d in range(num_d):
            policy['pi_{}'.format(A_D[d])] = D_s[d]

        return game_value[0], game_value[1], policy

class StackelbergEq(Strategy):
    def get_name(self):
        return 'SSE'

    def get_value(self, s, A_D, A_A, R_D, R_A, T, Q_D, Q_A):
        # Note: This is a simplified implementation using PuLP
        # The original Stackelberg equilibrium computation uses quadratic programming
        # which is more complex to implement with PuLP
        # This implementation uses a simpler approach that may not be as accurate
        
        num_d = len(A_D)
        num_a = len(A_A)
        
        # Get Defender/Leader's Q-value matrix
        M_D = []
        M_A = []
        for d in range(num_d):
            row_D = []
            row_A = []
            for a in range(num_a):
                k = '{}_{}_{}'.format(s, A_D[d], A_A[a])
                row_D.append(Q_D[k])
                row_A.append(Q_A[k])
            M_D.append(row_D)
            M_A.append(row_A)
        
        # Create a problem for each possible attacker pure strategy
        best_value_d = float('-inf')
        best_value_a = float('-inf')
        best_policy = {}
        
        for a_pure in range(num_a):
            # Create a linear program for defender's best response
            prob = self.lib.LpProblem(name=f'Stackelberg_{a_pure}', sense=self.lib.LpMaximize)
            
            # Defender's mixed strategy variables
            x = {}
            for d in range(num_d):
                x[d] = self.lib.LpVariable(name=f'x_{A_D[d]}', lowBound=0, upBound=1)
            
            # Objective: maximize defender's utility against this attacker pure strategy
            prob += self.lib.lpSum(x[d] * M_D[d][a_pure] for d in range(num_d))
            
            # Constraint: probabilities sum to 1
            prob += self.lib.lpSum(x[d] for d in range(num_d)) == 1
            
            # Constraint: this attacker strategy must be a best response
            for a_alt in range(num_a):
                if a_alt != a_pure:
                    # The attacker's utility for a_pure must be >= utility for a_alt
                    prob += self.lib.lpSum(x[d] * M_A[d][a_pure] for d in range(num_d)) >= \
                           self.lib.lpSum(x[d] * M_A[d][a_alt] for d in range(num_d))
            
            # Solve the problem
            prob.solve(self.lib.PULP_CBC_CMD(msg=False))
            
            # If feasible solution found
            if prob.status == self.lib.LpStatusOptimal:
                value_d = self.lib.value(prob.objective)
                value_a = sum(x[d].value() * M_A[d][a_pure] for d in range(num_d))
                
                # If this is the best defender value so far
                if value_d > best_value_d:
                    best_value_d = value_d
                    best_value_a = value_a
                    best_policy = {f'pi_{A_D[d]}': float(x[d].value()) for d in range(num_d)}
        
        # If no feasible solution was found, use uniform random strategy
        if not best_policy:
            p = 1.0 / num_d
            best_policy = {f'pi_{A_D[d]}': p for d in range(num_d)}
            best_value_d = sum(p * sum(M_D[d][a] / num_a for a in range(num_a)) for d in range(num_d))
            best_value_a = sum(p * sum(M_A[d][a] / num_a for a in range(num_a)) for d in range(num_d))
        
        return best_value_d, best_value_a, best_policy

def main():    
    agents = [UniformRandom(), NashEq(), StackelbergEq()]

    s_header = 'gamma '
    s = ''
    # s = 'gamma V0_ur V1_ur V2_ur V3_ur V0_n V1_n V2_n V3_n V0_s V1_s V2_s V3_s'
    for gamma in range(0, 100, 5):
        
        gamma = gamma/100.0
        s += '\n{} '.format(gamma)

        for agent in agents:
            
            agent.set_gamma(gamma)
            V, pi = agent.run()
            
            for state in V.keys():
                if '\n' not in s_header:
                    s_header += 'V{}_{} '.format(state, agent.get_name())
                s += '{} '.format(V[state])

        if '\n' not in s_header:
            s_header += '\n'

    s = s_header + s
    return s


if __name__ == '__main__':
    print(main())
