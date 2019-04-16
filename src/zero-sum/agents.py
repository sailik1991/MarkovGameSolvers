import numpy as np
from strategy import Strategy

__author__ = "Sailik Sengupta"

class MaxMinPure(Strategy):
    def get_value(self, s, A1, A2, R, T, Q):
        num_d = len(A1)
        num_a = len(A2)

        def_options = []
        policy = {}
        for d in range(num_d):
            def_options.append(
                        min(
                            [Q['{}_{}_{}'.format(s, A1[d], A2[a])] for a in range(num_a)]
                        )
                    )
            policy[A1[d]] = 0.0

        value = max(def_options)
        policy[A1[np.argmax(def_options)]] = 1.0

        return (float(value), policy)

class UniformRandom(Strategy):
    def get_value(self, s, A1, A2, R, T, Q):
        num_d = len(A1)
        num_a = len(A2)

        p = 1.0/num_d
        policy = {}
        for d in range(num_d):
            policy[A1[d]] = p

        min_v = +100000
        for a in range(num_a):
            v = 0
            for d in range(num_d):
                v += p * Q['{}_{}_{}'.format(s, A1[d], A2[a])]
            min_v = min(min_v, v)

        return(float(min_v), policy)

class OptimalMixed(Strategy):
    def get_value(self, s, A1, A2, R, T, Q):
        num_d = len(A1)
        num_a = len(A2)

        # Solve a optimization problem with Gurobi to find:
        # (1) The optimal value of the state (and update it)
        # (2) The optimal mixed strategy in the state
        m = self.lib.Model('LP')
        m.setParam('OutputFlag', 0)
        m.setParam('LogFile', '')
        m.setParam('LogToConsole', 0)
        v = m.addVar(name='v', vtype=self.lib.GRB.CONTINUOUS, lb=-1*self.lib.GRB.INFINITY)
        pi = {}
        for d in range(num_d):
            pi[d] = m.addVar(lb=0.0, ub=1.0, name='pi_{}'.format(A1[d]))
        m.update()
        for a in range(num_a):
            m.addConstr(
                self.lib.quicksum(pi[d] * Q['{}_{}_{}'.format(s, A1[d], A2[a])] for d in range(num_d)) >= v,
                name='c_ai_{}'.format(A2[a]))
        m.addConstr(self.lib.quicksum(pi[d] for d in range(num_d)) == 1, name='c_pi')
        m.setParam('DualReductions', 0)
        m.setObjective(v, sense=self.lib.GRB.MAXIMIZE)
        m.optimize()

        policy = {}
        for var in m.getVars():
            if 'pi_' in var.varName:
                policy[var.varName] = float(var.x)

        return (float(m.ObjVal), policy)

if __name__ == '__main__':
    agents = [UniformRandom(), OptimalMixed()]

    #s = 'gamma V0_mmp V1_mmp V2_mmp V3_mmp V0_ur V1_ur V2_ur V3_ur V0_om V1_om V2_om V3_om'
    s = 'gamma V0_ur V1_ur V2_ur V3_ur V0_om V1_om V2_om V3_om'
    for gamma in range(50, 100, 5):
        gamma = gamma/100.0
        s += '\n{} '.format(gamma)
        print( 'Discount Factor: {}'.format(gamma))
        for agent in agents:
            agent.set_gamma(gamma)
            V, pi = agent.run()
            #print(V)
            for state in V.keys():
                s += '{} '.format(V[state])
    print(s)

